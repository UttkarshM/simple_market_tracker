from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

# In-memory data since we can't use SQLite in serverless
COMPANIES = [
    {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries Limited', 'sector': 'Energy'},
    {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
    {'symbol': 'INFY.NS', 'name': 'Infosys Limited', 'sector': 'IT'},
    {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank Limited', 'sector': 'Banking'},
    {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank Limited', 'sector': 'Banking'},
    {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever Limited', 'sector': 'FMCG'},
    {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel Limited', 'sector': 'Telecom'},
    {'symbol': 'ITC.NS', 'name': 'ITC Limited', 'sector': 'FMCG'},
    {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank', 'sector': 'Banking'},
    {'symbol': 'LT.NS', 'name': 'Larsen & Toubro Limited', 'sector': 'Engineering'},
    {'symbol': 'WIPRO.NS', 'name': 'Wipro Limited', 'sector': 'IT'},
    {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India Limited', 'sector': 'Automotive'}
]

def fetch_stock_data(symbol, period='1mo'):
    """Fetch stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        stock_data = []
        for date, row in hist.iterrows():
            stock_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(row['Open'], 2),
                'high': round(row['High'], 2),
                'low': round(row['Low'], 2),
                'close': round(row['Close'], 2),
                'volume': int(row['Volume'])
            })
        
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return generate_mock_data(symbol)

def generate_mock_data(symbol, days=30):
    """Generate mock stock data if live data fails"""
    import random
    
    base_price = random.uniform(100, 2000)
    stock_data = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-i)).strftime('%Y-%m-%d')
        
        change = random.uniform(-0.05, 0.05) 
        base_price = max(base_price * (1 + change), 10) 
        open_price = base_price
        high_price = open_price * random.uniform(1.0, 1.03)
        low_price = open_price * random.uniform(0.97, 1.0)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(100000, 10000000)
        
        stock_data.append({
            'date': date,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
        
        base_price = close_price
    
    return stock_data

@app.route('/')
def index():
    """API status endpoint"""
    return jsonify({
        'message': 'Stock Market Dashboard API is running on Vercel!',
        'endpoints': {
            'companies': '/api/companies',
            'stock_data': '/api/stock/{symbol}',
            'stock_summary': '/api/stock/{symbol}/summary'
        },
        'status': 'online'
    })

@app.route('/api/companies')
def get_companies():
    """API endpoint to get list of companies"""
    return jsonify(COMPANIES)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    """API endpoint to get stock data for a specific company"""
    period = request.args.get('period', '1mo')
    
    try:
        stock_data = fetch_stock_data(symbol, period)
        
        return jsonify({
            'symbol': symbol,
            'data': stock_data,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/stock/<symbol>/summary')
def get_stock_summary(symbol):
    """API endpoint to get stock summary and key metrics"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        summary = {
            'symbol': symbol,
            'name': info.get('longName', 'N/A'),
            'currentPrice': info.get('currentPrice', 0),
            'previousClose': info.get('previousClose', 0),
            'dayHigh': info.get('dayHigh', 0),
            'dayLow': info.get('dayLow', 0),
            'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
            'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
            'volume': info.get('volume', 0),
            'avgVolume': info.get('averageVolume', 0),
            'marketCap': info.get('marketCap', 0),
            'sector': info.get('sector', 'N/A')
        }
        
        return jsonify(summary)
    
    except Exception as e:
        return jsonify({
            'symbol': symbol,
            'name': f'Mock Company ({symbol})',
            'currentPrice': 1250.50,
            'previousClose': 1245.30,
            'dayHigh': 1260.75,
            'dayLow': 1240.20,
            'fiftyTwoWeekHigh': 1350.00,
            'fiftyTwoWeekLow': 950.00,
            'volume': 2500000,
            'avgVolume': 2000000,
            'marketCap': 125000000000,
            'sector': 'Technology'
        })

# This is required for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

