# Deployment Guide

## Prerequisites

- Python 3.11+
- MongoDB 5.0+ (Atlas or self-hosted)
- Docker (optional, for containerized deployment)
- A hosting platform (Heroku, AWS, DigitalOcean, etc.)

## Local Development Setup

```bash
# Clone repository
git clone https://github.com/dpathak01/fast-api-secure-boilerplate.git
cd fast-api-secure-boilerplate

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate secure keys for development
python scripts/generate_keys.py

# Update .env with local settings
cp .env.example .env

# Start MongoDB (using Docker)
docker run -d -p 27017:27017 --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:7.0

# Run development server
APP_ENV=dev uvicorn app.main:app --reload

# Access API docs at http://localhost:8000/docs
```

## Docker Deployment

### Build Image

```bash
docker build -t fastapi-app:1.0 .
```

### Run Container

```bash
docker run -d \
  --name fastapi-api \
  -p 8000:8000 \
  -e APP_ENV=prod \
  -e MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net \
  -e MONGODB_DB_NAME=fastapi_db \
  -e JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))") \
  fastapi-app:1.0
```

## Docker Compose Deployment

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## AWS Deployment (EC2)

### 1. Create EC2 Instance

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Install Docker
sudo amazon-linux-extras install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
```

### 2. Deploy Application

```bash
# Clone repository
git clone https://github.com/dpathak01/fast-api-secure-boilerplate.git
cd fast-api-secure-boilerplate

# Setup environment
echo "APP_ENV=prod" > .env
echo "MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net" >> .env
echo "JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")" >> .env

# Build and run Docker image
docker build -t fastapi-app:1.0 .
docker run -d -p 8000:8000 --name fastapi-api fastapi-app:1.0
```

### 3. Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo yum install -y nginx

# Create config
sudo tee /etc/nginx/conf.d/fastapi.conf > /dev/null <<EOF
upstream fastapi {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Heroku Deployment

### 1. Setup Heroku

```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
heroku create your-app-name
```

### 2. Add MongoDB Atlas

1. Create cluster at [mongodb.com/cloud](https://www.mongodb.com/cloud/atlas)
2. Get connection string
3. Add to Heroku:

```bash
heroku config:set MONGODB_URL="mongodb+srv://user:pass@cluster..."
heroku config:set JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
heroku config:set APP_ENV=prod
```

### 3. Deploy

```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

## DigitalOcean Deployment (App Platform)

### 1. Create App

1. Go to DigitalOcean App Platform
2. Connect GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8080`

### 2. Add MongoDB

1. Create managed MongoDB in DigitalOcean
2. Add environment variables:
   - `APP_ENV`: prod
   - `MONGODB_URL`: Your connection string
   - `JWT_SECRET_KEY`: Generated secret

### 3. Deploy

Push to GitHub - deployment happens automatically.

## Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/fastapi-app

# Deploy
gcloud run deploy fastapi-app \
  --image gcr.io/PROJECT-ID/fastapi-app \
  --platform managed \
  --region us-central1 \
  --set-env-vars APP_ENV=prod,MONGODB_URL=mongodb+srv://...
```

## Environment Variables for Production

Set these securely in your hosting platform:

```env
APP_ENV=prod
DEBUG=False
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true
MONGODB_DB_NAME=fastapi_db_prod
JWT_SECRET_KEY=<generate-using-scripts/generate_keys.py>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]
```

## Security Checklist

- [ ] Use strong, randomly generated JWT_SECRET_KEY
- [ ] Enable HTTPS/TLS certificate (Let's Encrypt free)
- [ ] Set DEBUG=False in production
- [ ] Configure CORS_ORIGINS with actual domains
- [ ] Use environment variables (never hardcode secrets)
- [ ] Enable database authentication
- [ ] Setup database backups
- [ ] Configure logging and monitoring
- [ ] Use firewall rules to restrict access
- [ ] Implement rate limiting
- [ ] Setup SSL certificate renewal automation

## Monitoring and Logging

### Setup Application Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Monitor with Services

- **Error Tracking**: Sentry, Rollbar
- **Performance**: New Relic, Datadog
- **Logs**: CloudWatch, ELK Stack
- **Uptime**: Uptime Robot, PagerDuty

## Scaling Considerations

- Use multiple workers: `uvicorn app.main:app --workers 4`
- Implement database connection pooling
- Use CDN for static content
- Setup load balancer
- Consider async task queue (Celery)
- Implement caching (Redis)

## Troubleshooting

### MongoDB Connection Issues

```bash
# Check connection string
mongosh "mongodb+srv://username:password@cluster.mongodb.net/database"

# Verify credentials
```

### Application Not Starting

```bash
# Check logs
docker logs fastapi-api

# Verify environment variables
docker exec fastapi-api env
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip list --outdated
pip install --upgrade <package>

# Update requirements.txt
pip freeze > requirements.txt
```

### Database Maintenance

- Monitor disk space
- Setup automated backups
- Test backup restoration
- Clean old logs periodically

## Support

For deployment issues, consult the official documentation:
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MongoDB Connection](https://docs.mongodb.com/manual/reference/connection-string/)
- [Heroku Deployment](https://devcenter.heroku.com/)
