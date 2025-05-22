import requests
import os

# You can get a free API key at https://openrouter.ai
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Set this in your Railway environment variables

def interpret_tarot_cards(card_names):
    prompt = f"""
KEEP YOUR REPLY BRIEF! 2 sentences maximum! In the tone of a fortuneteller, provide an interpretation of these 3 tarot cards: {', '.join(card_names)}.
These cards are being drawn to decide whether or not a particular stock is wise to invest in. Decide if the cards are saying to BUY or SELL the stock.
You must mention all 3 cards by name.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # You can use anything here for testing
        "X-Title": "TarotStockPredictor"
    }

    body = {
        "model": "openchat/openchat-3.5",  # Free and great for chat-style prompts
        "messages": [
            {"role": "system", "content": "You are a mystical tarot fortuneteller."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    response.raise_for_status()

    return response.json()['choices'][0]['message']['content'].strip()