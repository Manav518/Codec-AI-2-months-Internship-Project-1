import argparse

from translator_engine import translate_text, translate_with_detection, SUPPORTED_LANGUAGES


def parse_args():
    parser = argparse.ArgumentParser(description="Translate a phrase into another language")
    parser.add_argument("--text", type=str, required=True,
                         help="The phrase you want translated")
    parser.add_argument("--to", type=str, required=True,
                         help="Language to translate INTO, e.g. spanish, french, hindi "
                              f"(supported: {', '.join(SUPPORTED_LANGUAGES.keys())})")
    parser.add_argument("--from", dest="from_lang", type=str, default=None,
                         help="Language the text is written in (optional - "
                              "auto-detected if you skip this)")
    return parser.parse_args()


def resolve_language_code(name_or_code):
    key = name_or_code.lower().strip()
    if key in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[key]
    return key  


def main():
    args = parse_args()
    target_code = resolve_language_code(args.to)

    if args.from_lang:
        source_code = resolve_language_code(args.from_lang)
        translated = translate_text(args.text, target_language=target_code,
                                     source_language=source_code)
        print(f"Original ({args.from_lang}): {args.text}")
        print(f"Translated ({args.to}): {translated}")
    else:
        result = translate_with_detection(args.text, target_language=target_code)
        print(f"Detected language: {result['detected_language_name']}")
        print(f"Original: {args.text}")
        print(f"Translated ({args.to}): {result['translated_text']}")


if __name__ == "__main__":
    main()
