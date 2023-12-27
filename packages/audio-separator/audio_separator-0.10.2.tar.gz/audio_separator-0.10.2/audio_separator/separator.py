import os
import warnings
import hashlib
import json
import logging
import warnings
import wget
import torch
import librosa
import numpy as np
import onnxruntime as ort
from pydub import AudioSegment
from audio_separator.utils import spec_utils


class Separator:
    def __init__(
        self,
        audio_file_path,
        log_level=logging.DEBUG,
        log_formatter=None,
        model_name="UVR_MDXNET_KARA_2",
        model_file_dir="/tmp/audio-separator-models/",
        output_dir=None,
        primary_stem_path=None,
        secondary_stem_path=None,
        output_format="WAV",
        output_subtype=None,
        normalization_enabled=True,
        denoise_enabled=True,
        output_single_stem=None,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.log_formatter = log_formatter

        self.log_handler = logging.StreamHandler()

        if self.log_formatter is None:
            self.log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

        self.log_handler.setFormatter(self.log_formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(self.log_handler)

        self.logger.info(
            f"Separator instantiating with input file: {audio_file_path}, model_name: {model_name}, output_dir: {output_dir}, output_format: {output_format}"
        )

        self.model_name = model_name
        self.model_file_dir = model_file_dir
        self.output_dir = output_dir
        self.primary_stem_path = primary_stem_path
        self.secondary_stem_path = secondary_stem_path

        # Create the model directory if it does not exist
        os.makedirs(self.model_file_dir, exist_ok=True)

        self.audio_file_path = audio_file_path
        self.audio_file_base = os.path.splitext(os.path.basename(audio_file_path))[0]

        self.model_name = model_name
        self.model_url = f"https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/{self.model_name}.onnx"
        self.model_data_url = "https://raw.githubusercontent.com/TRvlvr/application_data/main/mdx_model_data/model_data.json"

        self.output_subtype = output_subtype
        self.output_format = output_format

        if self.output_format is None:
            self.output_format = "WAV"

        if self.output_subtype is None and output_format == "WAV":
            self.output_subtype = "PCM_16"

        self.normalization_enabled = normalization_enabled
        if self.normalization_enabled:
            self.logger.debug(f"Normalization enabled, waveform will be normalized to max amplitude of 1.0 to avoid clipping.")
        else:
            self.logger.debug(f"Normalization disabled, waveform will not be normalized.")

        self.denoise_enabled = denoise_enabled
        if self.denoise_enabled:
            self.logger.debug(f"Denoising enabled, model will be run twice to reduce noise in output audio.")
        else:
            self.logger.debug(
                f"Denoising disabled, model will only be run once. This is twice as fast, but may result in noisier output audio."
            )

        self.output_single_stem = output_single_stem
        if output_single_stem is not None:
            if output_single_stem.lower() not in {"instrumental", "vocals"}:
                raise Exception("output_single_stem must be either 'instrumental' or 'vocals'")
            self.logger.debug(f"Single stem output requested, only one output file ({output_single_stem}) will be written")

        self.chunks = 0
        self.margin = 44100
        self.adjust = 1
        self.dim_c = 4
        self.hop = 1024

        self.primary_source = None
        self.secondary_source = None

        warnings.filterwarnings("ignore")
        self.cpu = torch.device("cpu")

        # Prepare for hardware-accelerated inference by validating both Torch and ONNX Runtime support either CUDA or CoreML
        self.logger.debug(f"Torch version: {str(torch.__version__)}")
        ort_device = ort.get_device()
        ort_providers = ort.get_available_providers()
        hardware_acceleration_enabled = False

        if torch.cuda.is_available():
            self.logger.info("CUDA is available in Torch, setting Torch device to CUDA")
            self.device = torch.device("cuda")

            if ort_device == "GPU" and "CUDAExecutionProvider" in ort_providers:
                self.logger.info("ONNXruntime has CUDAExecutionProvider available, enabling acceleration")
                self.onnx_execution_provider = ["CUDAExecutionProvider"]
                hardware_acceleration_enabled = True
            else:
                self.logger.warning("CUDAExecutionProvider not available in ONNXruntime, so acceleration will NOT be enabled")
                self.logger.warning("If you expect CUDA to work with your GPU, try pip install --force-reinstall onnxruntime-gpu")
        else:
            self.logger.debug("CUDA not available in Torch installation. If you expect GPU/CUDA support to work, please see README")

        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            self.logger.info("Apple Silicon MPS/CoreML is available in Torch, setting Torch device to MPS")

            # TODO: Change this to use MPS once FFTs are supported, see https://github.com/pytorch/pytorch/issues/78044
            # self.device = torch.device("mps")

            self.logger.warning("Torch MPS backend does not yet support FFT operations, Torch will still use CPU!")
            self.logger.warning("To track progress towards Apple Silicon acceleration, see https://github.com/pytorch/pytorch/issues/78044")
            self.device = torch.device("cpu")

            if "CoreMLExecutionProvider" in ort_providers:
                self.logger.info("ONNXruntime has CoreMLExecutionProvider available, enabling acceleration")
                self.onnx_execution_provider = ["CoreMLExecutionProvider"]
                hardware_acceleration_enabled = True
            else:
                self.logger.warning("CoreMLExecutionProvider not available in ONNXruntime, so acceleration will NOT be enabled")
                self.logger.warning("If you expect MPS/CoreML to work with your Mac, try pip install --force-reinstall onnxruntime-silicon")
        else:
            self.logger.debug("Apple Silicon MPS/CoreML not available in Torch installation. If you expect this to work, please see README")

        if not hardware_acceleration_enabled:
            self.logger.info("No hardware acceleration could be configured, running in CPU mode")
            self.device = torch.device("cpu")
            self.onnx_execution_provider = ["CPUExecutionProvider"]

    def get_model_hash(self, model_path):
        try:
            with open(model_path, "rb") as f:
                f.seek(-10000 * 1024, 2)
                return hashlib.md5(f.read()).hexdigest()
        except:
            return hashlib.md5(open(model_path, "rb").read()).hexdigest()

    def separate(self):
        model_path = os.path.join(self.model_file_dir, f"{self.model_name}.onnx")
        if not os.path.isfile(model_path):
            self.logger.debug(f"Model not found at path {model_path}, downloading...")
            wget.download(self.model_url, model_path)

        self.logger.debug("Reading model settings...")

        model_hash = self.get_model_hash(model_path)
        self.logger.debug(f"Model {model_path} has hash {model_hash} ...")

        model_data_path = os.path.join(self.model_file_dir, "model_data.json")
        if not os.path.isfile(model_data_path):
            self.logger.debug(f"Model data not found at path {model_data_path}, downloading...")
            wget.download(self.model_data_url, model_data_path)

        model_data_object = json.load(open(model_data_path))
        model_data = model_data_object[model_hash]

        self.compensate = model_data["compensate"]
        self.dim_f = model_data["mdx_dim_f_set"]
        self.dim_t = 2 ** model_data["mdx_dim_t_set"]
        self.n_fft = model_data["mdx_n_fft_scale_set"]
        self.primary_stem = model_data["primary_stem"]
        self.secondary_stem = "Vocals" if self.primary_stem == "Instrumental" else "Instrumental"

        self.logger.debug(
            f"Set model data values: compensate = {self.compensate} primary_stem = {self.primary_stem} dim_f = {self.dim_f} dim_t = {self.dim_t} n_fft = {self.n_fft}"
        )

        self.logger.debug("Loading model...")
        ort_ = ort.InferenceSession(model_path, providers=self.onnx_execution_provider)
        self.model_run = lambda spek: ort_.run(None, {"input": spek.cpu().numpy()})[0]

        self.initialize_model_settings()
        self.logger.info("Running inference...")
        mdx_net_cut = True
        mix, raw_mix, samplerate = prepare_mix(self.audio_file_path, self.chunks, self.margin, mdx_net_cut=mdx_net_cut)
        self.logger.info("Demixing...")
        source = self.demix_base(mix)[0]

        output_files = []

        if not isinstance(self.primary_source, np.ndarray):
            self.primary_source = spec_utils.normalize(self.logger, source, self.normalization_enabled).T

        if not isinstance(self.secondary_source, np.ndarray):
            raw_mix = self.demix_base(raw_mix, is_match_mix=True)[0] if mdx_net_cut else raw_mix
            self.secondary_source, raw_mix = spec_utils.normalize_two_stem(
                self.logger, source * self.compensate, raw_mix, self.normalization_enabled
            )
            self.secondary_source = -self.secondary_source.T + raw_mix.T

        if not self.output_single_stem or self.output_single_stem.lower() == self.primary_stem.lower():
            self.logger.info(f"Saving {self.primary_stem} stem...")
            if not self.primary_stem_path:
                self.primary_stem_path = os.path.join(
                    f"{self.audio_file_base}_({self.primary_stem})_{self.model_name}.{self.output_format.lower()}"
                )
            self.write_audio(self.primary_stem_path, self.primary_source, samplerate)
            output_files.append(self.primary_stem_path)

        if not self.output_single_stem or self.output_single_stem.lower() == self.secondary_stem.lower():
            self.logger.info(f"Saving {self.secondary_stem} stem...")
            if not self.secondary_stem_path:
                self.secondary_stem_path = os.path.join(
                    f"{self.audio_file_base}_({self.secondary_stem})_{self.model_name}.{self.output_format.lower()}"
                )
            self.write_audio(self.secondary_stem_path, self.secondary_source, samplerate)
            output_files.append(self.secondary_stem_path)

        if hasattr(torch, "cuda"):
            torch.cuda.empty_cache()

        return output_files

    def write_audio(self, stem_path, stem_source, samplerate):
        self.logger.debug(f"Entering write_audio with stem_path: {stem_path}, samplerate: {samplerate}")

        # Check if the numpy array is empty or contains very low values
        if np.max(np.abs(stem_source)) < 1e-6:
            self.logger.warning("Warning: stem_source array is near-silent or empty.")
            return

        # If output_dir is specified, create it and join it with stem_path
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)
            stem_path = os.path.join(self.output_dir, stem_path)

        self.logger.debug(f"Audio data shape before processing: {stem_source.shape}")
        self.logger.debug(f"Data type before conversion: {stem_source.dtype}")

        # Ensure the audio data is in the correct format (e.g., int16)
        if stem_source.dtype != np.int16:
            stem_source = (stem_source * 32767).astype(np.int16)
            self.logger.debug("Converted stem_source to int16.")

        # Correctly interleave stereo channels
        stem_source_interleaved = np.empty((2 * stem_source.shape[0],), dtype=np.int16)
        stem_source_interleaved[0::2] = stem_source[:, 0]  # Left channel
        stem_source_interleaved[1::2] = stem_source[:, 1]  # Right channel

        self.logger.debug(f"Interleaved audio data shape: {stem_source_interleaved.shape}")

        # Create a pydub AudioSegment
        try:
            audio_segment = AudioSegment(
                stem_source_interleaved.tobytes(), frame_rate=samplerate, sample_width=stem_source.dtype.itemsize, channels=2
            )
            self.logger.debug("Created AudioSegment successfully.")
        except Exception as e:
            self.logger.error(f"Error creating AudioSegment: {e}")
            return

        # Determine file format based on the file extension
        file_format = stem_path.lower().split(".")[-1]

        # For M4A files, specify 'mp4' as the container format
        if file_format == "m4a":
            file_format = "mp4"
        elif file_format == "mka":
            file_format = "matroska"

        # Export using the determined format
        try:
            audio_segment.export(stem_path, format=file_format)
            self.logger.debug(f"Exported audio file successfully to {stem_path}")
        except Exception as e:
            self.logger.error(f"Error exporting audio file: {e}")

    def initialize_model_settings(self):
        self.n_bins = self.n_fft // 2 + 1
        self.trim = self.n_fft // 2
        self.chunk_size = self.hop * (self.dim_t - 1)
        self.window = torch.hann_window(window_length=self.n_fft, periodic=False).to(self.device)
        self.freq_pad = torch.zeros([1, self.dim_c, self.n_bins - self.dim_f, self.dim_t]).to(self.device)
        self.gen_size = self.chunk_size - 2 * self.trim

    def initialize_mix(self, mix, is_ckpt=False):
        # Log the initial state of the mix
        self.logger.debug(f"Initializing mix. is_ckpt: {is_ckpt}, Initial mix shape: {mix.shape}")

        # Check if mix is a stereo (2-channel) signal
        if mix.shape[0] != 2:
            error_message = f"Expected a 2-channel audio signal, but got {mix.shape[0]} channels"
            self.logger.error(error_message)
            raise ValueError(error_message)

        if is_ckpt:
            self.logger.debug("Processing in checkpoint mode.")
            pad = self.gen_size + self.trim - (mix.shape[-1] % self.gen_size)
            self.logger.debug(f"Padding calculated: {pad}")
            mixture = np.concatenate((np.zeros((2, self.trim), dtype="float32"), mix, np.zeros((2, pad), dtype="float32")), 1)
            num_chunks = mixture.shape[-1] // self.gen_size
            self.logger.debug(f"Mixture shape after padding: {mixture.shape}, Number of chunks: {num_chunks}")
            mix_waves = [mixture[:, i * self.gen_size : i * self.gen_size + self.chunk_size] for i in range(num_chunks)]
        else:
            self.logger.debug("Processing in non-checkpoint mode.")
            mix_waves = []
            n_sample = mix.shape[1]
            pad = self.gen_size - n_sample % self.gen_size
            self.logger.debug(f"Number of samples: {n_sample}, Padding calculated: {pad}")
            mix_p = np.concatenate((np.zeros((2, self.trim)), mix, np.zeros((2, pad)), np.zeros((2, self.trim))), 1)
            self.logger.debug(f"Shape of mix after padding: {mix_p.shape}")

            i = 0
            while i < n_sample + pad:
                waves = np.array(mix_p[:, i : i + self.chunk_size])
                mix_waves.append(waves)
                i += self.gen_size
                self.logger.debug(f"Processed chunk {len(mix_waves)}: Start {i - self.gen_size}, End {i}")

        # Convert mix_waves to a PyTorch tensor and move it to the specified device
        mix_waves_tensor = torch.tensor(mix_waves, dtype=torch.float32).to(self.device)
        self.logger.debug(f"Converted mix_waves to tensor. Tensor shape: {mix_waves_tensor.shape}")

        return mix_waves_tensor, pad

    def demix_base(self, mix, is_ckpt=False, is_match_mix=False):
        chunked_sources = []
        for slice in mix:
            sources = []
            tar_waves_ = []
            mix_p = mix[slice]
            mix_waves, pad = self.initialize_mix(mix_p, is_ckpt=is_ckpt)
            mix_waves = mix_waves.split(1)
            pad = mix_p.shape[-1] if is_ckpt else -pad
            with torch.no_grad():
                for mix_wave in mix_waves:
                    tar_waves = self.run_model(mix_wave, is_ckpt=is_ckpt, is_match_mix=is_match_mix)
                    tar_waves_.append(tar_waves)
                tar_waves_ = np.vstack(tar_waves_)[:, :, self.trim : -self.trim] if is_ckpt else tar_waves_
                tar_waves = np.concatenate(tar_waves_, axis=-1)[:, :pad]
                start = 0 if slice == 0 else self.margin
                end = None if slice == list(mix.keys())[::-1][0] or self.margin == 0 else -self.margin
                sources.append(tar_waves[:, start:end] * (1 / self.adjust))
            chunked_sources.append(sources)
        sources = np.concatenate(chunked_sources, axis=-1)

        return sources

    def run_model(self, mix, is_ckpt=False, is_match_mix=False):
        spek = self.stft(mix.to(self.device)) * self.adjust
        spek[:, :, :3, :] *= 0

        if is_match_mix:
            spec_pred = spek.cpu().numpy()
        else:
            spec_pred = -self.model_run(-spek) * 0.5 + self.model_run(spek) * 0.5 if self.denoise_enabled else self.model_run(spek)

        if is_ckpt:
            return self.istft(spec_pred).cpu().detach().numpy()
        else:
            return (
                self.istft(torch.tensor(spec_pred).to(self.device))
                .to(self.cpu)[:, :, self.trim : -self.trim]
                .transpose(0, 1)
                .reshape(2, -1)
                .numpy()
            )

    def stft(self, x):
        x = x.reshape([-1, self.chunk_size])
        x = torch.stft(x, n_fft=self.n_fft, hop_length=self.hop, window=self.window, center=True, return_complex=True)
        x = torch.view_as_real(x)
        x = x.permute([0, 3, 1, 2])
        x = x.reshape([-1, 2, 2, self.n_bins, self.dim_t]).reshape([-1, self.dim_c, self.n_bins, self.dim_t])
        return x[:, :, : self.dim_f]

    def istft(self, x, freq_pad=None):
        freq_pad = self.freq_pad.repeat([x.shape[0], 1, 1, 1]) if freq_pad is None else freq_pad
        x = torch.cat([x, freq_pad], -2)
        x = x.reshape([-1, 2, 2, self.n_bins, self.dim_t]).reshape([-1, 2, self.n_bins, self.dim_t])
        x = x.permute([0, 2, 3, 1])
        x = x.contiguous()
        x = torch.view_as_complex(x)
        x = torch.istft(x, n_fft=self.n_fft, hop_length=self.hop, window=self.window, center=True)
        return x.reshape([-1, 2, self.chunk_size])


def prepare_mix(mix, chunk_set, margin_set, mdx_net_cut=False, is_missing_mix=False):
    samplerate = 44100

    if not isinstance(mix, np.ndarray):
        mix, samplerate = librosa.load(mix, mono=False, sr=44100)
    else:
        mix = mix.T

    if mix.ndim == 1:
        mix = np.asfortranarray([mix, mix])

    def get_segmented_mix(chunk_set=chunk_set):
        segmented_mix = {}

        samples = mix.shape[-1]
        margin = margin_set
        chunk_size = chunk_set * 44100
        assert not margin == 0, "margin cannot be zero!"

        if margin > chunk_size:
            margin = chunk_size
        if chunk_set == 0 or samples < chunk_size:
            chunk_size = samples

        counter = -1
        for skip in range(0, samples, chunk_size):
            counter += 1
            s_margin = 0 if counter == 0 else margin
            end = min(skip + chunk_size + margin, samples)
            start = skip - s_margin
            segmented_mix[skip] = mix[:, start:end].copy()
            if end == samples:
                break

        return segmented_mix

    segmented_mix = get_segmented_mix()
    raw_mix = get_segmented_mix(chunk_set=0) if mdx_net_cut else mix
    return segmented_mix, raw_mix, samplerate
