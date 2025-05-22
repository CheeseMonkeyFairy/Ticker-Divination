import requests
import os

# HARD-CODED API KEY FOR TESTING
OPENROUTER_API_KEY = "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"  # Replace with your key

print(f"🔍 Env check: API key found? {'YES' if OPENROUTER_API_KEY else 'NO'}")

def interpret_tarot_cards(card_names):
    print("🔮 Received tarot card names:", card_names)

    prompt = f"""
KEEP YOUR REPLY BRIEF! 2 sentences maximum! In the tone of a fortuneteller, provide an interpretation of these 3 tarot cards: {', '.join(card_names)}.
These cards are being drawn to decide whether or not a particular stock is wise to invest in. Decide if the cards are saying to BUY or SELL the stock.
You must mention all 3 cards by name.
"""
    print("📜 Prompt to send:", prompt)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Placeholder
        "X-Title": "TarotStockPredictor"
    }

    body = {
        "model": "mistralai/devstral-small:free",  # Free and great for chat-style prompts
        "messages": [
            {"role": "system", "content": "You are a mystical tarot fortuneteller."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print("🚀 Sending request to OpenRouter...")
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        print("📬 Response received")
        response.raise_for_status()

        content = response.json()['choices'][0]['message']['content'].strip()
        print("✅ LLM Response:", content)
        return content

    except requests.exceptions.HTTPError as e:
        print("❌ HTTP error occurred:", e)
        print("💬 Response text:", response.text)  # Show raw response
        return "An error occurred while interpreting the tarot cards."

    except Exception as e:
        print("❌ Other error occurred:", e)
        import traceback
        traceback.print_exc()
        return "An error occurred while interpreting the tarot cards."