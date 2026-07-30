from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException

from language_detector import detect_language

SUPPORTED_LANGUAGES = {
    "english": "en", "spanish": "es", "french": "fr", "german": "de",
    "hindi": "hi", "italian": "it", "portuguese": "pt", "russian": "ru",
    "japanese": "ja", "korean": "ko", "chinese": "zh-CN", "arabic": "ar",
    "bengali": "bn", "tamil": "ta", "telugu": "te", "marathi": "mr",
    "urdu": "ur", "turkish": "tr", "dutch": "nl", "polish": "pl",
}


def translate_text(text, target_language="en", source_language="auto"):
    if not text or not text.strip():
        return ""

    try:
        translated = GoogleTranslator(
            source=source_language, target=target_language
        ).translate(text)
        return translated
    except LanguageNotSupportedException as e:
        raise ValueError(f"Language not supported: {e}")
    except Exception as e:
        raise ConnectionError(
            f"Translation failed - check your internet connection. Details: {e}"
        )


def translate_with_detection(text, target_language="en"):
    code, name = detect_language(text)
    translated = translate_text(text, target_language=target_language, source_language="auto")
    return {
        "detected_language_code": code,
        "detected_language_name": name,
        "translated_text": translated,
    }


if __name__ == "__main__":
    result = translate_with_detection("Good morning, have a nice day!", target_language="es")
    print(f"Detected language: {result['detected_language_name']}")
    print(f"Translated text: {result['translated_text']}")
