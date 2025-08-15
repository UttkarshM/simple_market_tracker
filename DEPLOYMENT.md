# 🚀 Deployment Guide - Stock Market Dashboard

## Quick Start (Development)

### Prerequisites
- Python 3.8+ installed
- Node.js 14+ installed
- Git installed

### 1. Backend Setup (Flask API)

```bash
# Navigate to the project directory
cd jar

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask backend server
python app.py
```

The backend will start on `http://localhost:5000`

### 2. Frontend Setup (React)

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will start on `http://localhost:3000`

### 3. Test the Application

```bash
# In another terminal, test the API endpoints
python test_api.py
```

## 🐳 Docker Deployment (Bonus)

### Docker Setup

Create `Dockerfile` for the Flask backend:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Create `docker-compose.yml` for full stack:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./stock_data.db:/app/stock_data.db
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:5000
```

### Run with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## ☁️ Cloud Deployment Options

### Option 1: Railway

1. Push code to GitHub repository
2. Connect Railway to your GitHub account
3. Deploy both backend and frontend as separate services
4. Set environment variables for production

### Option 2: Render

1. Create two services on Render:
   - Web service for Flask backend
   - Static site for React frontend (after build)
2. Set build and start commands
3. Configure environment variables

### Option 3: Vercel + Heroku

1. Deploy React frontend to Vercel
2. Deploy Flask backend to Heroku
3. Update API URLs in frontend for production

## 🔧 Production Configuration

### Environment Variables

```bash
# Backend (.env)
FLASK_ENV=production
DATABASE_URL=sqlite:///stock_data.db
CORS_ORIGINS=https://your-frontend-domain.com

# Frontend (.env)
REACT_APP_API_URL=https://your-backend-domain.com/api
```

### Build Commands

```bash
# Frontend build
npm run build

# Backend production
gunicorn --bind 0.0.0.0:$PORT app:app
```

## 📊 Performance Optimization

1. **API Caching**: Implement Redis for stock data caching
2. **CDN**: Use CDN for static assets
3. **Database**: Upgrade to PostgreSQL for production
4. **Load Balancing**: Use nginx for load balancing

## 🧪 Testing in Production

```bash
# Health check endpoint
curl https://your-api-domain.com/api/companies

# Frontend check
curl https://your-frontend-domain.com
```

## 🛡️ Security Considerations

1. **HTTPS**: Enable SSL/TLS certificates
2. **CORS**: Restrict CORS origins in production
3. **Rate Limiting**: Implement API rate limiting
4. **Environment Variables**: Never commit sensitive data

## 📱 Mobile Optimization

The application is already responsive, but for better mobile experience:

1. **PWA**: Convert to Progressive Web App
2. **Service Workers**: Add offline capability
3. **App Shell**: Implement app shell architecture

## 🔍 Monitoring

### Health Checks

```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

### Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Analytics

- Google Analytics for frontend
- API usage tracking for backend
- Error monitoring with Sentry

## 🚀 Scaling Considerations

1. **Database**: PostgreSQL with connection pooling
2. **Cache**: Redis for session and data caching
3. **Queue**: Celery for background tasks
4. **Microservices**: Split into separate services
5. **Container Orchestration**: Kubernetes for large scale

## 📝 Deployment Checklist

- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Database initialized
- [ ] CORS configured for production
- [ ] Build process tested
- [ ] Health checks implemented
- [ ] SSL certificates configured
- [ ] Domain names configured
- [ ] Monitoring setup
- [ ] Backup strategy in place

---

For any deployment issues, check the logs and ensure all environment variables are properly configured.

