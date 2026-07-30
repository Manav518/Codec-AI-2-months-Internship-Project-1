import argparse
import datetime
import os

from translator_engine import translate_with_detection, SUPPORTED_LANGUAGES
from translate_text import resolve_language_code

TRANSLATIONS_DIR = "translations"


def parse_args():
    parser = argparse.ArgumentParser(description="Interactive phrase translator")
    parser.add_argument("--to", type=str, required=True,
                         help="Language to translate INTO, e.g. spanish, french, hindi "
                              f"(supported: {', '.join(SUPPORTED_LANGUAGES.keys())})")
    return parser.parse_args()


def main():
    args = parse_args()
    target_code = resolve_language_code(args.to)

    os.makedirs(TRANSLATIONS_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(TRANSLATIONS_DIR, f"session_{timestamp}.txt")

    print(f"Interactive Translator - translating into: {args.to}")
    print("Type a phrase and press Enter. Type 'quit' to stop.\n")

    log_lines = []

    while True:
        text = input("You: ").strip()
        if text.lower() in ("quit", "exit"):
            break
        if not text:
            continue

        try:
            result = translate_with_detection(text, target_language=target_code)
            print(f"  [{result['detected_language_name']}] -> {result['translated_text']}\n")
            log_lines.append(f"{text}  ->  {result['translated_text']}")
        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}\n")

    if log_lines:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
        print(f"\nSession saved to: {log_path}")

    print("Goodbye!")


if __name__ == "__main__":
    main()
