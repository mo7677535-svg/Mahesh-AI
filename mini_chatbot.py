"""
Mini AI Chatbot (FREE - Google Gemini) - made by Mahesh Oli
Run in VS Code: open this file and press F5 (or type: python mini_chatbot.py)
"""

import os
import re
import time
from google import genai
from google.genai import types

try:
    from dotenv import load_dotenv
    load_dotenv()  # reads GEMINI_API_KEY from the .env file
except ImportError:
    pass

SYSTEM_PROMPT = (
    "You are a smart, friendly AI assistant. Anyone can ask you anything and you give a "
    "clear, helpful answer. You were made by Mahesh Oli. Only if someone asks who "
    "made/created/built YOU, answer: 'I was made by Mahesh Oli.' "
    "You can help with every topic: school subjects (English, Maths, Science, Social Studies, "
    "Accountancy, Economics, Nepali, Computer), general knowledge, writing letters and essays, "
    "coding, career and study advice, translation, and everyday questions. "
    "Rules: "
    "1) Use simple, easy words and explain like a good teacher. "
    "2) For Maths and Accountancy, solve step by step and show the final answer clearly. "
    "3) For definitions, give a short definition first, then one simple example. "
    "4) Reply in the same language the person uses: Nepali question gets a Nepali answer, "
    "English question gets an English answer. "
    "5) Keep answers short unless the person asks for a long answer, essay or full explanation. "
    "6) For questions about places (where is X located), always answer with the place type, district, province and country, plus nearby well-known places or the direction from a big city. Places in Nepal are very common, so answer them confidently. "
    "7) Never reply with an empty answer. If you are not sure, say what you do know and say honestly what you are unsure about. "
    "8) Answer the question in the latest message. Do not mix in earlier topics unless the person clearly refers to them."
)

# If one model is busy (503) or unavailable (404), the bot tries the next one
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash-lite"]

api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "paste-your-key-here":
    api_key = input("Paste your Gemini API key and press Enter: ").strip()

client = genai.Client(api_key=api_key)
history = []  # conversation memory


def is_maker_question(text: str) -> bool:
    """True only when the person asks who made THE BOT (not 'who built the pyramids')."""
    t = text.lower()
    about_bot = re.search(
        r"\b(who|whom)\b.*\b(made|make|created|create|built|build|developed|develop|designed|programmed|owns|own)\b.*\b(you|u|yourself)\b",
        t,
    )
    direct = re.search(r"\b(your|ur)\s+(creator|maker|developer|owner|builder)\b", t)
    return bool(about_bot or direct)


CONFIG = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3)


def ask_stream(user_message: str):
    """Gives the answer piece by piece, so the first words appear quickly."""
    if is_maker_question(user_message):
        yield "I was made by Mahesh Oli."
        return

    history.append(types.Content(role="user", parts=[types.Part(text=user_message)]))
    answer = ""
    last_error = None
    try:
        for model in MODELS:  # busy or broken model? switch to the next one right away
            try:
                for chunk in client.models.generate_content_stream(
                    model=model, contents=history, config=CONFIG
                ):
                    piece = chunk.text or ""
                    if piece:
                        answer += piece
                        yield piece
            except Exception as e:
                last_error = e
            if answer.strip():
                break
            if last_error is None:
                last_error = Exception("The AI gave an empty answer. Please ask again in other words.")
        if not answer.strip():
            raise last_error
    finally:
        if answer.strip():
            history.append(types.Content(role="model", parts=[types.Part(text=answer)]))
        else:
            history.pop()  # do not keep a failed question in memory


def ask(user_message: str) -> str:
    return "".join(ask_stream(user_message))


def main():
    print("=" * 56)
    print(" Mini AI Chatbot (made by Mahesh Oli)")
    print(" Ask me anything: school subjects, general")
    print(" knowledge, writing, coding, and more.")
    print(" Type 'quit' to exit.")
    print("=" * 56 + "\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Bot: Goodbye!")
            break
        if not user_input:
            continue
        try:
            print("Bot: ", end="", flush=True)
            for piece in ask_stream(user_input):
                print(piece, end="", flush=True)
            print("\n")
        except Exception as e:
            print("\nError:", e, "\n")


if __name__ == "__main__":
    main()
