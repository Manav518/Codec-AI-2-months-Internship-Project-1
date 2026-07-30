from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0
LANGUAGE_NAMES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "hi": "Hindi", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
    "ja": "Japanese", "ko": "Korean", "zh-cn": "Chinese", "ar": "Arabic",
    "bn": "Bengali", "ta": "Tamil", "te": "Telugu", "mr": "Marathi",
    "ur": "Urdu", "tr": "Turkish", "nl": "Dutch", "pl": "Polish",
}


def detect_language(text):
    if not text or not text.strip():
        return "unknown", "Unknown"

    try:
        code = detect(text)
    except LangDetectException:
        return "unknown", "Unknown"

    name = LANGUAGE_NAMES.get(code, code)
    return code, name


if __name__ == "__main__":
    samples = [
        "Hello, how are you today?",
        "Hola, como estas?",
        "Bonjour, comment ca va?",
        "Namaste, aap kaise hain?",
    ]
    for text in samples:
        code, name = detect_language(text)
        print(f"'{text}' -> {name} ({code})")
