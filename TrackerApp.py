import requests
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Tarot API URL
api_url = 'https://tarotapi.dev/api/v1/cards/random?n=3'  # Fetch 3 random cards

# List of popular stock tickers (you can add more if needed)
popular_tickers = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT', 'NFLX', 'SPY', 'GOOG', 'META', 'NVDA']

# Function to fetch stock data from Yahoo Finance
def fetch_stock_data(ticker):
    stock_data = yf.download(ticker, period="1y", interval="1d")
    return stock_data

# Function to plot stock data
def plot_stock_data(stock_data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Closing Price')
    plt.title(f'{ticker} Stock Price Over the Last Year')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)

    # Save the plot as a PNG image in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Convert the plot to a base64 string for rendering in HTML
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

# Function to fetch 3 random tarot cards and return the card details and corresponding image filenames
def fetch_random_tarot_cards():
    try:
        # Request 3 random tarot cards from the Tarot API
        response = requests.get(api_url)
        response.raise_for_status()  # Check if request was successful
        card_data = response.json()
        cards = card_data['cards']  # Get the list of cards

        tarot_cards = []
        for card in cards:
            card_name = card['name']
            card_name_short = card['name_short']  # This corresponds to the image filename

            # Construct the filename for the card image
            image_filename = f"{card_name_short}.jpg"  # Match the image file name to 'name_short'

            # Append card details along with the image filename
            tarot_cards.append({
                'name': card_name,
                'meaning_up': card['meaning_up'],
                'meaning_rev': card['meaning_rev'],
                'desc': card['desc'],
                'image': image_filename
            })

        # Randomly choose a "BUY!" or "SELL!" message
        action_message = random.choice(["BUY! BUY! BUY!", "SELL! SELL! SELL!"])

        # Return the list of tarot cards along with the action message
        return tarot_cards, action_message

    except requests.exceptions.RequestException as e:
        print(f"Error fetching tarot cards: {e}")
        return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    stock_image = None
    ticker = None
    tarot_cards = None
    action_message = None
    
    if request.method == "POST":
        # If the "Random Ticker" button is pressed
        if 'random_ticker' in request.form:
            ticker = random.choice(popular_tickers)  # Randomly choose a ticker
        else:
            ticker = request.form.get("ticker")  # Get stock ticker input if entered

        # Fetch stock data if a ticker is chosen (either random or input by user)
        if ticker:
            stock_data = fetch_stock_data(ticker)
            stock_image = plot_stock_data(stock_data, ticker)
        
        # Fetch 3 random tarot cards and the action message
        tarot_cards, action_message = fetch_random_tarot_cards()
    
    return render_template("index.html", stock_image=stock_image, ticker=ticker, tarot_cards=tarot_cards, action_message=action_message)

if __name__ == "__main__":
    app.run(debug=True)