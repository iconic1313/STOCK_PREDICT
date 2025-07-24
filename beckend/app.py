# from flask import   Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# import matplotlib.pyplot as plt
# #initialize flask and enable cors

# app =Flask(__name__)
# CORS(app)

# def get_stock_data(ticker_symbol):
#     try:
#         df = yf.download(ticker_symbol, start='2018-01-01', auto_adjust=True)
#         if df.empty:
#             raise ValueError("No data found for the ticker symbol.")
# df['SMA_10'] = df['Close'].rolling(window=10).mean()
# df['SMA_20'] = df['Close'].rolling(window=20).mean()


# df.dropna(inplace=True)

# X = df[['Open', 'High', 'Low', 'Volume', 'SMA_10', 'SMA_20']]
# y = df['Close']

# model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
# model.fit(X, y)

# latest_data = X.iloc[-1:]
# predicted_price = model.predict(latest_data)
# actual_price = y.iloc[-1].item()

# print(f"📊 {symbol} - Today's Actual Closing Price: ${actual_price:.2f}")
# print(f"📈 {symbol} - Predicted Next Closing Price: ${predicted_price[0]:.2f}")

# plt.figure(figsize=(14, 6))
# plt.plot(df['Close'].tail(100), label='Actual Close (last 100 days)', color='blue')
# plt.axhline(predicted_price[0], color='orange', linestyle='--', label='Predicted Next Close')
# plt.title('varshil Stock Price Prediction (U.S based)')
# plt.xlabel('Date')
# plt.ylabel('Price ($)')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import traceback
import os

# Initialize Flask app
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing to allow the React frontend to connect
CORS(app)

# --- Main Prediction Function ---
def get_prediction_data(ticker_symbol):
    """
    Fetches live data, trains a simple model, makes a prediction,
    and returns it in the format expected by the frontend.
    """
    try:
        print(f"\n📡 [1/5] Fetching info for {ticker_symbol}...")
        stock_info = yf.Ticker(ticker_symbol)
        info = stock_info.info

        # --- Get Live Price and Company Name ---
        # Use .get() to avoid errors if a key is missing
        company_name = info.get('longName', ticker_symbol)
        # Find the most reliable current price
        live_price = info.get('currentPrice') or info.get('regularMarketPreviousClose')
        
        if not live_price:
            print(f"❌ Could not determine a live price for {ticker_symbol}.")
            return None
        
        print(f"✅ Live Price: {live_price}, Company: {company_name}")

        # --- Get Historical Data for Training ---
        print(f"📡 [2/5] Fetching historical data (5 years)...")
        # Fetch a substantial amount of data for training
        df = stock_info.history(period="5y", auto_adjust=True)

        if df.empty:
            print(f"❌ Historical data for {ticker_symbol} is empty.")
            return None
        print(f"✅ Data fetched: {len(df)} rows")

        # --- Feature Engineering ---
        print("🛠️ [3/5] Performing feature engineering...")
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()
        df.dropna(inplace=True) # Remove rows with NaN values after SMA calculation
        
        if df.empty:
            print(f"❌ Data became empty after feature engineering. Not enough data for a 30-day SMA.")
            return None

        # --- Model Training ---
        print("🧠 [4/5] Training prediction model...")
        # Define features (X) and target (y)
        features = ['Open', 'High', 'Low', 'Volume', 'SMA_10', 'SMA_30']
        X = df[features]
        y = df['Close']
        
        # Initialize and train the model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        print("✅ Model trained.")

        # --- Make Prediction ---
        print("🔮 [5/5] Making prediction...")
        # Use the very last row of data to predict the next day's price
        last_row = X.iloc[[-1]]
        predicted_price = model.predict(last_row)[0]
        
        print(f"📊 Prediction: {predicted_price:.2f}, Live Price: {live_price:.2f}")

        # --- Construct Final JSON Response ---
        # This structure MUST match what the frontend expects
        result = {
            "companyName": company_name,
            "ticker": ticker_symbol,
            "price": round(live_price, 2),
            "prediction": {
                "value": round(predicted_price, 2),
                # Add emoji for a nice touch
                "trend": "Bullish 🐂" if predicted_price > live_price else "Bearish 🐻",
            }
        }
        return result

    except Exception as e:
        print(f"❌ An error occurred for ticker {ticker_symbol}:")
        # Print the full error traceback to the terminal for debugging
        traceback.print_exc()
        return None

# --- API Route ---
@app.route('/predict', methods=['GET'])
def predict():
    # Get the ticker symbol from the URL query parameter (e.g., ?ticker=AAPL)
    ticker = request.args.get('ticker')
    print(f"\n\n🚀 Received request for ticker: {ticker}")

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    # Call the main function to get the data
    data = get_prediction_data(ticker.upper())
    
    if data:
        # If successful, return the data as JSON with a 200 OK status
        return jsonify(data)
    else:
        # If it failed, return an error message with a 404 Not Found status
        return jsonify({"error": f"Could not fetch or process data for '{ticker}'. It may be an invalid symbol."}), 404

# --- Run Server ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)