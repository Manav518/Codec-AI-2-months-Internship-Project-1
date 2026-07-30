# Language Translator (Simple NLP Phrase Translator)

A simple tool that translates phrases from one language to another —
and can even figure out what language you typed in automatically.

## What's in this project

```
language_translator/
├── language_detector.py         # Figures out what language your text is in
├── translator_engine.py          # The "brain" that does the actual translating
├── translate_text.py               # Run this to translate ONE phrase
├── interactive_translator.py    # Run this to chat/translate phrase after phrase
├── requirements.txt              # List of tools to install
├── translations/                     # (created automatically) saved translation logs
└── README.md
```

You only ever run **`translate_text.py`** or **`interactive_translator.py`** yourself.
The other two files are helpers they use behind the scenes.

## How it works (in plain words)

1. You type a phrase (e.g. "Hello, how are you?")
2. The tool guesses what language it's written in (English, Spanish, Hindi, etc.)
3. It sends the phrase to Google's free translation service over the internet
4. It gets back the translated phrase and shows it to you

**You need an internet connection** for the actual translating part (step 3) — only the language-guessing part (step 2) works without internet.

## Step 1: Install Python (skip if you already have it)

Check first:
```
python --version
```
If that shows an error, download Python from https://www.python.org/downloads/ and install it (tick "Add Python to PATH" on Windows).

## Step 2: Make a project folder

Create a folder called `language_translator` (e.g. on your Desktop). Put all 5 project files (`language_detector.py`, `translator_engine.py`, `translate_text.py`, `interactive_translator.py`, `requirements.txt`) inside it.

## Step 3: Open a terminal inside that folder

- **Windows**: open the folder in File Explorer → click the address bar → type `cmd` → press Enter
- **Mac**: right-click the folder → "New Terminal at Folder"

## Step 4: Install the libraries

```
pip install -r requirements.txt
```
This installs two things:
- `deep-translator` — does the actual translating (uses Google Translate for free, no account/API key needed)
- `langdetect` — guesses what language your text is written in

Wait for it to finish, then move to the next step.

## Step 5: Translate your first phrase

Type this into your terminal:
```
python translate_text.py --text "Hello, how are you?" --to spanish
```

You should see something like:
```
Detected language: English
Original: Hello, how are you?
Translated (spanish): Hola, ¿cómo estás?
```

Try changing the phrase and the `--to` language, for example:
```
python translate_text.py --text "Thank you so much" --to french
python translate_text.py --text "Good morning" --to hindi
```

**Supported language names you can use after `--to`:** english, spanish, french, german, hindi, italian, portuguese, russian, japanese, korean, chinese, arabic, bengali, tamil, telugu, marathi, urdu, turkish, dutch, polish.

## Step 6 (optional): Translate phrase after phrase, like a chat

If you don't want to type a whole command every time, use the interactive version:
```
python interactive_translator.py --to spanish
```
Then just type phrases one at a time and press Enter — it translates each one instantly. Type `quit` when you're done. Everything you translated gets saved into the `translations` folder.

## Troubleshooting

- **"Translation failed - check your internet connection"**: this tool needs internet access to reach Google's translation service — make sure you're connected.
- **Detected language looks wrong for a very short phrase**: language guessing is harder with just 1-2 words (e.g. "OK" could be many languages) — it works best on full sentences.
- **`pip` not recognized**: make sure Python installed correctly with "Add to PATH" checked (Step 1).

## How It Works (Concepts)

- **NLP (Natural Language Processing)**: the field of AI focused on understanding and working with human language.
- **Language detection**: analyzing patterns of letters/words to guess which language a text is written in.
- **Machine translation**: using large trained models (like Google Translate's) to convert meaning from one language's words into another's.

## Possible Extensions
- Add a simple web page (Streamlit) with a text box and a dropdown for languages.
- Add support for translating whole text files, not just single phrases.
- Add a "detect and translate to my language automatically" mode.
