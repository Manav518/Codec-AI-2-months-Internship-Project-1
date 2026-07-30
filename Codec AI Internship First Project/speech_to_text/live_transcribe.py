import argparse
import datetime
import os

import speech_recognition as sr

TRANSCRIPTS_DIR = "transcripts"


def parse_args():
    parser = argparse.ArgumentParser(description="Live microphone transcription")
    parser.add_argument("--language", type=str, default="en-US",
                         help="Language code, e.g. en-US, hi-IN, es-ES (default: en-US)")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    session_lines = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(TRANSCRIPTS_DIR, f"live_session_{timestamp}.txt")

    print("Calibrating for background noise... please stay quiet for a second.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Ready! Start speaking. Press Ctrl+C to stop.\n")

    try:
        while True:
            with mic as source:
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language=args.language)
                print(f"You said: {text}")
                session_lines.append(text)
            except sr.UnknownValueError:
                print("[Could not understand audio - try speaking clearly]")
            except sr.RequestError as e:
                print(f"[Speech service error: {e}. Check your internet connection.]")

    except KeyboardInterrupt:
        print("\n\nStopped listening.")
        full_text = " ".join(session_lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Session transcript saved to: {output_path}")


if __name__ == "__main__":
    main()
