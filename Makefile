.PHONY: help install dev qa prod docker-dev docker-build clean test lint format

help:
	@echo "FastAPI Secure Boilerplate - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Run development server"
	@echo "  make qa             Run QA server"
	@echo "  make prod           Run production server"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run all tests"
	@echo "  make test-unit      Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Lint code"
	@echo "  make format         Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-dev     Run with Docker Compose"
	@echo "  make docker-build   Build Docker image"
	@echo ""
	@echo "Database:"
	@echo "  make db-start       Start MongoDB container"
	@echo "  make db-stop        Stop MongoDB container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove cache files and venv"

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Dependencies installed"

dev:
	APP_ENV=dev uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

qa:
	APP_ENV=qa uvicorn app.main:app --host 0.0.0.0 --port 8000

prod:
	APP_ENV=prod uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

test:
	pytest -v

test-unit:
	pytest -v -m unit

test-integration:
	pytest -v -m integration

lint:
	python -m pylint app/

format:
	python -m black app/ tests/

docker-dev:
	docker-compose up -d
	@echo "✓ Docker Compose started"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/docs"
	@echo "  MongoDB: localhost:27017"

docker-build:
	docker build -t fastapi-app:1.0 .
	@echo "✓ Docker image built"

db-start:
	docker run -d --name mongodb -p 27017:27017 \
	  -e MONGO_INITDB_ROOT_USERNAME=root \
	  -e MONGO_INITDB_ROOT_PASSWORD=password \
	  mongo:7.0
	@echo "✓ MongoDB started"

db-stop:
	docker stop mongodb || true
	docker rm mongodb || true
	@echo "✓ MongoDB stopped"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	rm -rf venv/
	@echo "✓ Cleaned up"
