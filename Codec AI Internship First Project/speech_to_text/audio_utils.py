import os
from pydub import AudioSegment

SUPPORTED_INPUT_FORMATS = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"]


def convert_to_wav(input_path, output_path=None):
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED_INPUT_FORMATS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported types: {SUPPORTED_INPUT_FORMATS}"
        )

    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + "_converted.wav"

    audio = AudioSegment.from_file(input_path)

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)

    audio.export(output_path, format="wav")
    return output_path


def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0  


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        wav_path = convert_to_wav(test_file)
        print(f"Converted file saved to: {wav_path}")
        print(f"Duration: {get_audio_duration(wav_path):.2f} seconds")
    else:
        print("Usage: python audio_utils.py <path_to_audio_file>")
