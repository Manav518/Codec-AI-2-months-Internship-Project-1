import argparse
import os

from transcriber import transcribe_audio_file

TRANSCRIPTS_DIR = "transcripts"


def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe an audio file to text")
    parser.add_argument("--audio", type=str, required=True,
                         help="Path to the audio file (mp3, wav, m4a, ogg, flac)")
    parser.add_argument("--language", type=str, default="en-US",
                         help="Language code, e.g. en-US, hi-IN, es-ES (default: en-US)")
    parser.add_argument("--output", type=str, default=None,
                         help="Path to save the transcript .txt file "
                              "(default: transcripts/<audiofilename>.txt)")
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.audio):
        raise FileNotFoundError(f"Audio file not found: {args.audio}")

    os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.audio))[0]
        args.output = os.path.join(TRANSCRIPTS_DIR, f"{base_name}.txt")

    print(f"Transcribing: {args.audio}")
    print(f"Language: {args.language}\n")

    transcript = transcribe_audio_file(args.audio, language=args.language)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("\n--- Full Transcript ---")
    print(transcript if transcript.strip() else "[No speech detected]")
    print(f"\nTranscript saved to: {args.output}")


if __name__ == "__main__":
    main()
