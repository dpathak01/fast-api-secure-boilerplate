#!/bin/bash

# Production-grade run script for FastAPI application

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
ENV="${APP_ENV:-dev}"
PORT="${PORT:-8000}"
WORKERS="${WORKERS:-1}"

# Print header
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   FastAPI Secure Boilerplate          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check MongoDB connection
echo -e "${YELLOW}Checking MongoDB connection...${NC}"
python3 -c "
from app.database import db_connection
try:
    db_connection.connect()
    print('✓ MongoDB connection successful')
except Exception as e:
    print(f'✗ MongoDB connection failed: {e}')
    exit(1)
"

echo ""
echo -e "${GREEN}Starting FastAPI application${NC}"
echo -e "${GREEN}Environment: ${BLUE}${ENV}${NC}"
echo -e "${GREEN}Port: ${BLUE}${PORT}${NC}"
echo -e "${GREEN}Workers: ${BLUE}${WORKERS}${NC}"
echo ""
echo -e "${YELLOW}API Docs: http://localhost:${PORT}/docs${NC}"
echo ""

# Run application based on environment
if [ "$ENV" = "dev" ]; then
    uvicorn app.main:app --reload --host 0.0.0.0 --port "$PORT"
else
    uvicorn app.main:app --workers "$WORKERS" --host 0.0.0.0 --port "$PORT"
fi
