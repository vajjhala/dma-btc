import yfinance as yf
import requests
from datetime import datetime

def calculate_dma(ticker, days):
    data = yf.download(ticker, period='1mo')
    data['DMA'] = data['Close'].rolling(window=days).mean()
    return data

def generate_signal(live_price, dma):
    if live_price > dma:
        return "buy"
    else:
        return "sell"
    
def get_live_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    return response.json()['bitcoin']['usd']

data = calculate_dma('BTC-USD', 23)
dma = data['DMA'].iloc[-1]
dma_date = data.index[-1].strftime('%Y-%m-%d') # Date of the last DMA calculation

live_price = get_live_price()
live_price_date = datetime.now().strftime('%Y-%m-%d') # Current date

print(f"23-DMA at {dma_date:16} : {dma:.2f}")
print(f"Live Price at {live_price_date:12} : {live_price:.2f}")

signal = generate_signal(live_price, dma)
print(f"Signal : {signal}")