from typing import IO

from transformers import WhisperForConditionalGeneration, WhisperProcessor

from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel
from speech_recognition_api.extra.audio_utils import audio_bytes_to_np_array, file_to_audio_segment


class WhisperModel(ISpeechRecognitionModel):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.processor = WhisperProcessor.from_pretrained(self.model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(self.model_name)

    def process_file(self, file: IO) -> str:
        audio = file_to_audio_segment(file, set_channels=1, set_sample_rate=16000)
        samples = audio_bytes_to_np_array(audio.raw_data)
        input_features = self.processor(
            samples,
            sampling_rate=audio.frame_rate,
            return_tensors="pt",
        ).input_features
        predicted_ids = self.model.generate(input_features)
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()

    @classmethod
    def build_from_config(cls) -> "WhisperModel":
        from speech_recognition_api.extra.whisper_model.config import whisper_config  # noqa: PLC0415

        return cls(model_name=whisper_config.name)
