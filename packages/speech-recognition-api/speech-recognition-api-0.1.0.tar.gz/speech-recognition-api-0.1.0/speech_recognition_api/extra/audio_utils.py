from typing import IO, Optional

import numpy as np
from pydub import AudioSegment


def audio_bytes_to_np_array(audio_bytes: bytes) -> np.ndarray:
    return (
        np.frombuffer(
            audio_bytes,
            np.int16,
        )
        .flatten()
        .astype(np.float32)
        / 32768.0
    )  # No idea what this number means :)


def file_to_audio_segment(
    file: IO, *, set_channels: Optional[int] = 1, set_sample_rate: Optional[int] = 16000
) -> AudioSegment:
    audio = AudioSegment.from_file(file)
    audio = audio.set_channels(set_channels)
    return audio.set_frame_rate(set_sample_rate)
