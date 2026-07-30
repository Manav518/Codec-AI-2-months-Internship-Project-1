import json
import random
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.3


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()


class ChatBot:
    def __init__(self, intents_path="intents.json"):
        with open(intents_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.intents = data["intents"]

        self.all_patterns = []
        self.pattern_tags = []
        for intent in self.intents:
            for pattern in intent["patterns"]:
                self.all_patterns.append(clean_text(pattern))
                self.pattern_tags.append(intent["tag"])

        self.vectorizer = TfidfVectorizer()
        self.pattern_vectors = self.vectorizer.fit_transform(self.all_patterns)

        self.responses_by_tag = {
            intent["tag"]: intent["responses"] for intent in self.intents
        }

    def get_response(self, user_input):
        cleaned = clean_text(user_input)
        if not cleaned:
            return "Please type something so I can respond!"

        input_vector = self.vectorizer.transform([cleaned])

        similarities = cosine_similarity(input_vector, self.pattern_vectors)[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]

        if best_score < SIMILARITY_THRESHOLD:
            tag = "fallback"
        else:
            tag = self.pattern_tags[best_index]

        return random.choice(self.responses_by_tag[tag])


if __name__ == "__main__":
    bot = ChatBot()
    for test_input in ["hi there", "what's your name", "tell me a joke", "asdkjaskjd"]:
        print(f"You: {test_input}")
        print(f"Bot: {bot.get_response(test_input)}\n")
