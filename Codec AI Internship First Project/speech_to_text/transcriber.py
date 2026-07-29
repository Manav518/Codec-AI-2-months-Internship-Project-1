import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

from audio_utils import convert_to_wav


def transcribe_audio_file(file_path, language="en-US", show_progress=True):
    ext = os.path.splitext(file_path)[1].lower()
    if ext != ".wav":
        if show_progress:
            print(f"Converting {ext} file to WAV format...")
        wav_path = convert_to_wav(file_path)
    else:
        wav_path = file_path

    audio = AudioSegment.from_wav(wav_path)

    chunks = split_on_silence(
        audio,
        min_silence_len=500,     
        silence_thresh=audio.dBFS - 14, 
        keep_silence=250,          
    )

    if not chunks:
        chunks = [audio]

    recognizer = sr.Recognizer()
    full_text = []

    os.makedirs("temp_chunks", exist_ok=True)

    for i, chunk in enumerate(chunks, start=1):
        chunk_path = os.path.join("temp_chunks", f"chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")

        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language=language)
            full_text.append(text)
            if show_progress:
                print(f"  Chunk {i}/{len(chunks)}: {text}")
        except sr.UnknownValueError:

            if show_progress:
                print(f"  Chunk {i}/{len(chunks)}: [could not understand audio]")
        except sr.RequestError as e:
            raise ConnectionError(
                f"Could not reach the speech recognition service: {e}. "
                "Check your internet connection."
            )
        finally:
            os.remove(chunk_path)

    if os.path.isdir("temp_chunks") and not os.listdir("temp_chunks"):
        os.rmdir("temp_chunks")

    return " ".join(full_text)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = transcribe_audio_file(sys.argv[1])
        print("\n--- Full Transcript ---")
        print(result)
    else:
        print("Usage: python transcriber.py <path_to_audio_file>")
