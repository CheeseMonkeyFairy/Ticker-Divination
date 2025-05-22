import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise EnvironmentError("❌ Missing TOGETHER_API_KEY in environment variables.")
else:
    print("✅ TOGETHER_API_KEY is set:", TOGETHER_API_KEY[:5] + "...")

def interpret_tarot_cards(card_names):
    print("🔮 Received tarot card names:", card_names)

    prompt = f"""
KEEP YOUR REPLY BRIEF! 2 sentences maximum! In the tone of a fortuneteller, provide an interpretation of these 3 tarot cards: {', '.join(card_names)}.
These cards are being drawn to decide whether or not a particular stock is wise to invest in. Decide if the cards are saying to BUY or SELL the stock.
You must mention all 3 cards by name.
"""

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": f"You are a mystical tarot fortuneteller.\n{prompt}",
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=body)
        response.raise_for_status()
        return response.json()['choices'][0]['text'].strip()
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP error:", e)
        print("💬 Raw response:", response.text)
        return "An error occurred while interpreting the tarot cards."
    except Exception as e:
        print("❌ Other error:", e)
        return "An error occurred while interpreting the tarot cards."