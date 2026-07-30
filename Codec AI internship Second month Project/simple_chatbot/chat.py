import datetime
import os

from chatbot_engine import ChatBot

LOGS_DIR = "chat_logs"


def main():
    print("Loading chatbot...")
    bot = ChatBot()
    print("Chatbot is ready! Type 'quit' to exit.\n")

    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOGS_DIR, f"chat_{timestamp}.txt")
    log_lines = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Bot: Goodbye!")
            break
        if not user_input:
            continue

        response = bot.get_response(user_input)
        print(f"Bot: {response}\n")

        log_lines.append(f"You: {user_input}")
        log_lines.append(f"Bot: {response}")

    if log_lines:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))
        print(f"Conversation saved to: {log_path}")


if __name__ == "__main__":
    main()
