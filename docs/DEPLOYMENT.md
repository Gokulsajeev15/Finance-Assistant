# Deployment Guide

## Development Deployment

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd Finance-Assistant
cp .env.example .env
# Edit .env with your OpenAI API key

# Start development environment
./manage.sh dev
```

### Manual Development Setup

#### Backend Only
```bash
# Install Python dependencies
uv sync

# Start backend
./manage.sh start
# OR manually:
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Only
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## Production Deployment

### 1. Build Frontend
```bash
./manage.sh build
# OR manually:
cd frontend && npm run build
```

### 2. Environment Configuration

Create production `.env`:
```env
OPENAI_API_KEY=your_production_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Backend Deployment Options

#### Option A: Direct Uvicorn
```bash
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Option B: Gunicorn + Uvicorn Workers
```bash
pip install gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Option C: Docker
```bash
# Build image
docker build -t finance-assistant ./backend

# Run container
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  finance-assistant
```

### 4. Frontend Deployment Options

#### Option A: Static File Server
```bash
# After building frontend
cd frontend/dist
python -m http.server 5173
# OR
npx serve -s . -l 5173
```

#### Option B: Nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Cloud Deployment

### Heroku

#### Backend (Heroku)
1. Create `Procfile`:
```
web: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

2. Configure buildpack:
```bash
heroku buildpacks:set heroku/python
```

3. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_key_here
```

#### Frontend (Netlify/Vercel)
1. Connect your repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Configure redirects for SPA in `public/_redirects`:
```
/*    /index.html   200
```

### AWS

#### Backend (AWS Lambda + API Gateway)
```bash
# Install serverless framework
npm install -g serverless

# Deploy
serverless deploy
```

#### Frontend (AWS S3 + CloudFront)
```bash
# Upload build files to S3
aws s3 sync frontend/dist/ s3://your-bucket-name/

# Configure CloudFront for SPA routing
```

### Google Cloud Platform

#### Backend (Cloud Run)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Deploy to Cloud Run
gcloud run deploy finance-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Frontend (Firebase Hosting)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Initialize and deploy
firebase init hosting
firebase deploy
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional
- `OPENAI_MODEL`: AI model to use (default: gpt-4o-mini)

## Monitoring and Maintenance

### Health Checks
- Backend: `GET /` returns health status
- Frontend: Check if page loads correctly

### Log Monitoring
```bash
# View backend logs
tail -f backend.log

# View access logs (if using nginx)
tail -f /var/log/nginx/access.log
```

### Performance Monitoring
- Monitor API response times
- Check stock data API rate limits
- Monitor OpenAI API usage and costs

### Backup and Recovery
- Environment variables backup
- Code repository backup
- No persistent database to backup

## Security Considerations

### Production Security Checklist
- [ ] Use HTTPS in production
- [ ] Secure OpenAI API key storage
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting (if needed)
- [ ] Monitor API usage and costs
- [ ] Regular dependency updates

### Environment Security
```env
# Use secure environment variable management
OPENAI_API_KEY=sk-...  # Never commit this to git
```

## Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check port availability
lsof -i :8000

# Check Python environment
uv run python --version

# Check dependencies
uv sync
```

#### API Errors
```bash
# Test APIs manually
curl http://localhost:8000/docs

# Check OpenAI API key
curl http://localhost:8000/api/v1/ai/chat \
  -X POST -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

#### Frontend Build Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Issues
- Check external API rate limits (Yahoo Finance, OpenAI)
- Monitor memory usage for large company databases
- Optimize frontend bundle size if needed

## Scaling Considerations

### Backend Scaling
- Add Redis for caching company data
- Implement proper database for persistent storage
- Add load balancing for multiple instances
- Implement rate limiting and request queuing

### Frontend Scaling
- Use CDN for static assets
- Implement service worker for offline support
- Add progressive loading for large datasets
- Optimize bundle splitting and lazy loading

### Cost Optimization
- Monitor OpenAI API usage and implement caching
- Use efficient Yahoo Finance API calls
- Implement request batching where possible
- Consider using cheaper AI models for basic queries
