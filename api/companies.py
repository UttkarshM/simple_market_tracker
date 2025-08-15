from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        companies = [
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
        
        response = json.dumps(companies)
        self.wfile.write(response.encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

