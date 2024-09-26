from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def remove_silence(audio_path, silence_thresh=-16, min_silence_len=500):
    """Remove silence from the beginning and end of an audio file."""
    audio = AudioSegment.from_file(audio_path)
    dBFS = audio.dBFS
    silence_threshold = dBFS + silence_thresh
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

    if nonsilent_ranges:
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[-1][1]
        trimmed_audio = audio[start_trim:end_trim]
    else:
        trimmed_audio = audio

    return trimmed_audio

