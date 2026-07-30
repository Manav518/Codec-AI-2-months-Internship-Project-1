# Simple Chatbot

A chatbot that can hold a basic conversation and answer simple questions —
runs entirely on your computer, no internet needed.

## What's in this project

```
simple_chatbot/
├── intents.json          # The bot's "knowledge" - example phrases + replies
├── chatbot_engine.py    # The "brain" that matches your text to a reply
├── chat.py                    # Run this to actually chat with the bot
├── requirements.txt      # List of tools to install
├── chat_logs/                 # (created automatically) saved conversations
└── README.md
```

You only ever run **`chat.py`** yourself. The other files are what it uses behind the scenes.

## How it works (in plain words)

The bot doesn't "understand" language like a human. Instead:

1. `intents.json` has a list of **topics** (like "greeting," "goodbye," "joke"), and for each topic, a few **example phrases** ("hi", "hello", "hey") and a few **possible replies**.
2. When you type something, the bot compares your words to every example phrase it knows, and finds the closest match.
3. It picks one of the replies from that matching topic.
4. If nothing matches well enough, it says something like "I don't understand."

This is called a **rule-based chatbot** — simple, fast, and doesn't need internet or a massive AI model, but it only knows what's inside `intents.json`.

## Step 1: Make a project folder

Create a folder called `simple_chatbot` (e.g. on your Desktop). Put all 4 files (`intents.json`, `chatbot_engine.py`, `chat.py`, `requirements.txt`) inside it.

## Step 2: Open a terminal inside that folder

- **Windows**: open the folder → click the address bar → type `cmd` → press Enter
- **Mac**: right-click the folder → "New Terminal at Folder"

## Step 3: Install the one library it needs

```
pip install -r requirements.txt
```
This installs `scikit-learn`, a library used to compare how similar two sentences are.

## Step 4: Start chatting

```
python chat.py
```

You'll see:
```
Loading chatbot...
Chatbot is ready! Type 'quit' to exit.

You: 
```

Now just type things and press Enter, for example:
```
You: hi
Bot: Hello! How can I help you today?

You: what is your name
Bot: You can call me Chatbot. I'm here to chat with you.

You: tell me a joke
Bot: Why do Python programmers wear glasses? Because they can't C.
```

Type `quit` when you're done — it'll save the whole conversation into a `chat_logs` folder.

## Step 5: Teach it new things (this is the fun part!)

Open `intents.json` in any text editor (Notepad works fine). You'll see blocks like this:
```json
{
  "tag": "joke",
  "patterns": ["tell me a joke", "say something funny"],
  "responses": ["Why don't programmers like nature? It has too many bugs."]
}
```
- **`patterns`**: example ways someone might phrase that request. Add more so the bot recognizes more variations.
- **`responses`**: possible replies — add more, and the bot will pick a random one each time so it feels less repetitive.

You can also add a whole new topic by copying one of these blocks, changing the `tag` name, and writing your own patterns/responses. Save the file and run `python chat.py` again to try it.

## Troubleshooting

- **"Sorry, I didn't quite get that" for everything you type**: the bot only recognizes phrases similar to what's in `intents.json` — try adding more example patterns for the topics you want it to understand.
- **JSON errors when running chat.py**: if you edited `intents.json` and it now fails to load, you probably have a typo (a missing comma or quote). Double check your edits match the same style as the existing entries.

## How It Works (Concepts)

- **Intent matching**: recognizing what category/topic a piece of text belongs to.
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: a way of turning sentences into numbers based on which words are most meaningful in them, so they can be mathematically compared.
- **Cosine similarity**: a way of measuring how "close" two of those number-sentences are — the closer, the more similar the meaning.
- **Fallback response**: a default reply used when nothing matches well, so the bot never just stays silent or crashes.

## Possible Extensions
- Add more intents/topics to make it smarter.
- Build a simple web chat interface instead of the terminal.
- Upgrade to a more advanced AI model (like a transformer-based chatbot) for open-ended conversations.
