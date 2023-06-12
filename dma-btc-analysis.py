import pandas as pd
import numpy as np
import yfinance as yf

def calculate_dma(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data['DMA'] = data['Close'].rolling(window=23).mean()
    return data

def simulate_investment(data, initial_investment):
    in_position = False
    btc_holdings = 0
    usd_holdings = initial_investment

    for i in range(len(data)):
        # Skip the first 22 days when the DMA is not available
        if i < 22:
            continue
        
        # If we're not in a position and the closing price is above DMA, buy BTC
        if not in_position and data['Close'].iloc[i] > data['DMA'].iloc[i]:
            btc_holdings = usd_holdings / data['Close'].iloc[i]
            usd_holdings = 0
            in_position = True
        # If we're in a position and the closing price is below DMA, sell BTC
        elif in_position and data['Close'].iloc[i] < data['DMA'].iloc[i]:
            usd_holdings = btc_holdings * data['Close'].iloc[i]
            btc_holdings = 0
            in_position = False

    # If we're still in a position at the end of the period, sell BTC
    if in_position:
        usd_holdings = btc_holdings * data['Close'].iloc[-1]
    
    return usd_holdings

# Fetch the data and calculate DMA
data = calculate_dma('BTC-USD', '2023-04-14', '2023-06-05')

# Simulate the investment
final_value = simulate_investment(data, 2000)

print(f"Final value of the investment: {final_value}")
