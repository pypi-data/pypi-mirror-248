from typing import BinaryIO

import numpy as np

SAMPLE_RATE = 48000


def resample_from_file(io: "BinaryIO") -> tuple["np.ndarray", float]:
    import warnings
    import librosa
    warnings.warn("resample_from_file is deprecated, use dfpwm.resample instead")
    return librosa.load(io, dtype='float32', sr=SAMPLE_RATE)


def resample(data: np.ndarray, origin_samplerate: float, target_sample_rate=SAMPLE_RATE):
    import librosa
    return librosa.resample(data, origin_samplerate, target_sample_rate)
