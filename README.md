# 📈 Stock Market Dashboard

A Flask/React application for visualizing Indian stock market data with real-time charts and company information.

## 🚀 Quick Start

### Backend (Flask)
```bash
pip install -r requirements.txt
python app.py  # Runs on http://localhost:5000
```

### Frontend (React)
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Docker
```bash
docker-compose up --build
```

## 📊 Features

- Real-time stock data via Yahoo Finance API
- Interactive price charts with Chart.js
- Company profiles and market metrics
- SQLite database for data persistence
- Responsive Bootstrap UI

## 🔌 API Endpoints

- `GET /api/companies` - List all companies
- `GET /api/stock/{symbol}` - Get stock price data
- `GET /api/stock/{symbol}/summary` - Get company metrics

## 🏢 Supported Companies

- **IT**: TCS, Infosys, Wipro
- **Banking**: HDFC Bank, ICICI Bank, Kotak Mahindra Bank
- **Energy**: Reliance Industries
- **FMCG**: Hindustan Unilever, ITC
- **Others**: Bharti Airtel (Telecom), L&T (Engineering), Maruti Suzuki (Auto)

## 📘 Tech Stack

- **Backend**: Flask, SQLite, yfinance, Pandas
- **Frontend**: React, Bootstrap, Chart.js, Axios
- **DevOps**: Docker, Docker Compose

## 📁 Project Structure

```
jar/
├── app.py               # Flask backend
├── requirements.txt     # Python dependencies
├── Dockerfile           # Backend container
├── docker-compose.yml   # Container orchestration
├── stock_data.db        # Database
├── frontend/            # React frontend
```

## 🔧 Troubleshooting

- **Backend**: Ensure Python 3.9+ and port 5000 available
- **Frontend**: Check Node.js 14+ and backend connection
- **Docker**: Verify Docker is running and ports available

See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment options.

---

*This dashboard provides educational content only. Always consult with financial professionals before investing.*

