# FastAPI Secure Boilerplate

A production-grade FastAPI REST CRUD API boilerplate with JWT authentication, CORS, MongoDB integration, and environment-based configuration (dev, QA, prod).

## Features

✅ **Modular Architecture** - Clean, scalable project structure  
✅ **MongoDB Integration** - Async MongoDB with connection pooling  
✅ **JWT Authentication** - Secure token-based authentication  
✅ **CORS Configuration** - Environment-aware CORS settings  
✅ **Security Best Practices** - Password hashing, security headers, input validation  
✅ **Environment Management** - Dev, QA, and Production configurations  
✅ **Docker Support** - Docker & Docker Compose for containerization  
✅ **Comprehensive Error Handling** - Proper HTTP status codes and error messages  
✅ **Input Validation** - Pydantic models with email validation  

## Project Structure

```
fast-api-secure-boilerplate/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Environment-based configuration
│   ├── database.py          # MongoDB connection management
│   ├── models.py            # Pydantic schemas
│   ├── security.py          # JWT and password utilities
│   ├── middleware.py        # CORS and security middleware
│   └── routes/
│       ├── __init__.py
│       └── users.py         # User CRUD endpoints
├── .env                     # Default local environment
├── .env.example             # Example environment template
├── .env.dev                 # Development environment
├── .env.qa                  # QA environment
├── .env.prod                # Production environment
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image
├── docker-compose.yml       # Docker Compose for local dev
├── .gitignore
└── readme.md

```

## Prerequisites

- Python 3.11+
- MongoDB 5.0+ (local or Atlas)
- Docker & Docker Compose (optional)

## Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/dpathak01/fast-api-secure-boilerplate.git
cd fast-api-secure-boilerplate

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

By default, the application loads `.env`. This is the recommended local setup when your MongoDB Atlas URL is already configured in `.env`.

```bash
# Optional: create a local .env from the example template
cp .env.example .env
```

Update these values in `.env`:

```env
ENV=dev
DEBUG=True
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=fastapi_db
JWT_SECRET_KEY=dev-secret-key-change-in-production
```

Set `APP_ENV` only when you intentionally want to load one of the environment-specific files:

```bash
# Loads .env.dev
export APP_ENV=dev

# Loads .env.qa
export APP_ENV=qa

# Loads .env.prod
export APP_ENV=prod
```

If you want the app to use `.env`, do not set `APP_ENV`. If it is already set in your shell, run `unset APP_ENV` before starting the server.

### 3. MongoDB Setup

#### Option A: Local MongoDB

```bash
# Using Docker Compose
docker-compose up -d

# Or install MongoDB locally and run
mongod
```

#### Option B: MongoDB Atlas (Cloud)

1. Create cluster at [mongodb.com/cloud](https://www.mongodb.com/cloud/atlas)
2. Update `MONGODB_URL` in `.env` for local development:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
3. If you are using an environment-specific file, update the matching file instead, such as `.env.dev` or `.env.prod`.

### 4. Run Application

```bash
# Local development using .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# If APP_ENV is already exported and you want to use .env
unset APP_ENV
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Development using .env.dev
APP_ENV=dev uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# QA using .env.qa
APP_ENV=qa uvicorn app.main:app --host 0.0.0.0 --port 8000

# Production using .env.prod
APP_ENV=prod uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

`make dev` uses `APP_ENV=dev`, so it loads `.env.dev`. Use the direct `uvicorn` command above when you want to run with `.env`.

## API Documentation

Automatic interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

If `/docs` opens as a blank page after changing middleware or environment settings, restart the Uvicorn process and hard refresh the browser. Swagger UI and ReDoc load JavaScript and CSS from `cdn.jsdelivr.net`, and the security middleware allows those assets on `/docs` and `/redoc`.

## API Endpoints

### Health Check
```
GET /health
```

### Authentication

#### Register
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "secure_password_123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### Login
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password_123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### User CRUD

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <access_token>

Response:
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Get User by ID
```http
GET /api/v1/users/{user_id}

Response: (same as above)
```

#### Update User
```http
PUT /api/v1/users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "is_active": true
}

Response: (updated user)
```

#### Delete User
```http
DELETE /api/v1/users/{user_id}
Authorization: Bearer <access_token>

Response: 204 No Content
```

## Configuration

### Environment Variables

Create `.env` for local development, or create `.env.<environment>` files for explicit environments selected by `APP_ENV`:

```env
# Environment
ENV=dev
DEBUG=True/False

# Server
HOST=0.0.0.0
PORT=8000

# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=fastapi_db_dev

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=["*"]
CORS_ALLOW_HEADERS=["*"]
```

`APP_ENV` is a shell selector used by the config loader. It is not required inside `.env`.

### Security Headers

Automatically added by the security middleware:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy: default-src 'self'`

In production, the middleware also adds:
- `Strict-Transport-Security: max-age=31536000`

For API documentation routes, the Content Security Policy is relaxed only enough to allow Swagger UI and ReDoc assets from `cdn.jsdelivr.net`.

## Security Features

1. **Password Security**
   - Bcrypt hashing with salt
   - Minimum 8 characters required
   - Verified on login

2. **JWT Authentication**
   - Configurable expiration
   - Secure token generation
   - Token validation on protected routes

3. **Input Validation**
   - Email validation
   - Type checking with Pydantic
   - Request body validation

4. **Authorization**
   - Users can only update/delete their own profiles
   - Role-based access control (extensible)

5. **CORS Protection**
   - Environment-specific origins
   - Configurable allowed methods and headers
   - Credentials support

## Docker Deployment

### Development with Docker Compose

```bash
docker-compose up -d
```

This starts:
- FastAPI application on port 8000
- MongoDB on port 27017

### Production Deployment

```bash
# Build image
docker build -t fastapi-app:1.0 .

# Run with environment
docker run -d \
  --name fastapi-app \
  -p 8000:8000 \
  -e APP_ENV=prod \
  -e MONGODB_URL=mongodb+srv://... \
  -e JWT_SECRET_KEY=your-secret \
  fastapi-app:1.0
```

## Testing Examples

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Get user (replace TOKEN and USER_ID)
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

## Production Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Update `MONGODB_URL` to production database
- [ ] Set `DEBUG=False`
- [ ] Configure `CORS_ORIGINS` with actual domains
- [ ] Update security headers for your domain
- [ ] Enable HTTPS/TLS
- [ ] Use environment-specific credentials
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test all endpoints thoroughly

## Extending the API

### Add New Routes

1. Create new file in `app/routes/`
2. Define routes using FastAPI router
3. Import and include in `app/main.py`

Example:

```python
# app/routes/products.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

@router.get("/{product_id}")
async def get_product(product_id: str):
    # Implementation
    pass
```

Then in `app/main.py`:
```python
from app.routes import products
app.include_router(products.router)
```

### Add New Collections

Update MongoDB collections in your routes by using `db["collection_name"]`.

## License

MIT License

## Support

For issues, questions, or suggestions, please open an issue in the repository.
