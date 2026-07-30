# Speech-to-Text Transcription Tool

A simple tool that turns spoken audio into written text — either from an
audio file (like an MP3 recording) or live from your microphone.

## What's in this project

```
speech_to_text/
├── audio_utils.py         # Converts audio files into the right format
├── transcriber.py          # The core "brain" that turns audio into text
├── transcribe_file.py     # Run this to transcribe an audio FILE
├── live_transcribe.py     # Run this to transcribe your MICROPHONE live
├── requirements.txt      # List of tools/libraries to install
├── transcripts/                # (created automatically) saved text results
└── README.md
```

You only ever run **`transcribe_file.py`** or **`live_transcribe.py`** directly.
The other two files are "helpers" they use behind the scenes.

## How it actually works (in plain words)

1. Your audio (file or microphone) gets recorded as sound data.
2. That sound is sent to Google's free speech recognition service over the internet (the same tech behind Google's voice typing).
3. Google sends back the text of what was said.
4. The tool prints it and saves it to a `.txt` file.

**You need an internet connection for this to work**, since the free recognizer used here (`recognize_google`) sends the audio over the web to be processed.

## Step 1: Install Python

Check if it's already installed:
```
python3 --version
```
If not, download it from https://www.python.org/downloads/ (on Windows, tick "Add Python to PATH" during setup).

## Step 2: Download the project files

Save all the files listed above into one folder, e.g. `speech_to_text` on your Desktop.

## Step 3: Install one extra system tool: ffmpeg

The library that converts audio formats (MP3 → WAV) needs a free tool called **ffmpeg**.

- **Windows**: Download from https://www.gyan.dev/ffmpeg/builds/ (get the "essentials" build), unzip it, and add its `bin` folder to your system PATH. (Search "how to add to PATH Windows" if you're unsure — it's a one-time setup.)
- **Mac**: Open Terminal and run:
  ```
  brew install ffmpeg
  ```
  (If you don't have `brew`, install it first from https://brew.sh)
- **Linux**: 
  ```
  sudo apt install ffmpeg
  ```

Check it worked:
```
ffmpeg -version
```
You should see version info, not an error.

## Step 4: Open a terminal inside your project folder

- **Windows**: open the folder → click the address bar → type `cmd` → Enter
- **Mac**: right-click the folder → "New Terminal at Folder"

## Step 5: Install the Python libraries

```
pip install -r requirements.txt
```

**Note for microphone use only:** `PyAudio` (needed for live microphone transcription) sometimes fails to install directly. If it does:
- **Windows**: run `pip install pipwin` then `pipwin install pyaudio`
- **Mac**: run `brew install portaudio` first, then re-run `pip install -r requirements.txt`
- **Linux**: run `sudo apt install python3-pyaudio` first

If you only want to transcribe audio *files* (not live microphone), you can skip PyAudio entirely — just remove that line from `requirements.txt` before installing.

## Step 6: Transcribe an audio file

Put an audio file (mp3, wav, m4a, ogg, or flac) in your project folder — e.g. `recording.mp3`. Then run:
```
python3 transcribe_file.py --audio recording.mp3
```

What you'll see:
- It converts the file to the right format
- It splits the audio into chunks wherever there's a pause in speech
- It prints each chunk's text as it's recognized
- At the end it prints and saves the full transcript to `transcripts/recording.txt`

## Step 7 (optional): Transcribe your microphone live

```
python3 live_transcribe.py
```
- It'll calibrate to your room's background noise for a second
- Then say "Ready! Start speaking."
- Speak a sentence, pause — it prints what it heard
- Keep speaking as many sentences as you like
- Press `Ctrl+C` when done — it saves everything said into `transcripts/live_session_<timestamp>.txt`

## Using a different language

Both scripts accept a `--language` flag with a language code, for example:
```
python3 transcribe_file.py --audio recording.mp3 --language hi-IN
python3 live_transcribe.py --language es-ES
```
Common codes: `en-US` (English/US), `en-GB` (English/UK), `hi-IN` (Hindi), `es-ES` (Spanish), `fr-FR` (French), `de-DE` (German).

## Troubleshooting

- **"Could not understand audio"**: the audio was too quiet, noisy, or silent in that section — that's normal for pauses/background noise, not necessarily an error.
- **"Could not reach the speech recognition service"**: check your internet connection — this tool needs it.
- **PyAudio install errors**: see Step 5's notes above — this is the most common hiccup, and it's OS-specific.
- **ffmpeg not found errors**: make sure Step 3 is done correctly and `ffmpeg -version` works in your terminal.

## How It Works (Concepts)

- **Speech Recognition**: software that converts spoken audio waveforms into text by matching sound patterns to words.
- **Chunking on silence**: long audio is split wherever there's a quiet gap (a pause between sentences), since recognizing short clips is more accurate than one giant file.
- **Sample rate / mono conversion**: speech recognizers expect audio in a specific format (16kHz, single audio channel), so files are converted automatically.

## Possible Extensions
- Add a simple web interface (Streamlit) with a "record" button and file upload.
- Try an offline recognizer (like Vosk) so it works without internet.
- Add speaker labels for conversations with multiple people.
