from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  

DATABASE = 'stock_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            sector TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            volume INTEGER,
            FOREIGN KEY (symbol) REFERENCES companies (symbol)
        )
    ''')
    
    companies = [
        ('RELIANCE.NS', 'Reliance Industries Limited', 'Energy'),
        ('TCS.NS', 'Tata Consultancy Services', 'IT'),
        ('INFY.NS', 'Infosys Limited', 'IT'),
        ('HDFCBANK.NS', 'HDFC Bank Limited', 'Banking'),
        ('ICICIBANK.NS', 'ICICI Bank Limited', 'Banking'),
        ('HINDUNILVR.NS', 'Hindustan Unilever Limited', 'FMCG'),
        ('BHARTIARTL.NS', 'Bharti Airtel Limited', 'Telecom'),
        ('ITC.NS', 'ITC Limited', 'FMCG'),
        ('KOTAKBANK.NS', 'Kotak Mahindra Bank', 'Banking'),
        ('LT.NS', 'Larsen & Toubro Limited', 'Engineering'),
        ('WIPRO.NS', 'Wipro Limited', 'IT'),
        ('MARUTI.NS', 'Maruti Suzuki India Limited', 'Automotive')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO companies (symbol, name, sector) 
        VALUES (?, ?, ?)
    ''', companies)
    
    conn.commit()
    conn.close()

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
    """Serve the React frontend"""
    return jsonify({
        'message': 'Stock Market Dashboard API is running!',
        'endpoints': {
            'companies': '/api/companies',
            'stock_data': '/api/stock/{symbol}',
            'stock_summary': '/api/stock/{symbol}/summary'
        },
        'frontend': 'http://localhost:3000 (development)'
    })

@app.route('/api/companies')
def get_companies():
    """API endpoint to get list of companies"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT symbol, name, sector FROM companies ORDER BY name')
    companies = cursor.fetchall()
    
    conn.close()
    
    result = [
        {
            'symbol': company[0],
            'name': company[1],
            'sector': company[2]
        }
        for company in companies
    ]
    
    return jsonify(result)

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

if __name__ == '__main__':
    init_db()
    print("Stock Market Dashboard API is starting...")
    print("Database initialized with sample companies")
    app.run(debug=True, host='0.0.0.0', port=5000)

