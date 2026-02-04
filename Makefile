.PHONY: help run-backend run-frontend run-docker

help:
	@echo "Doccoon - Available commands:"
	@echo ""
	@echo "  make run-backend    Start the Django backend server"
	@echo "  make run-frontend   Start the Vue.js frontend dev server"
	@echo "  make run-docker     Build and start all services with Docker"
	@echo "  make help           Show this help message"

run-backend:
	cd doccoon_backend && uv run python manage.py runserver

run-frontend:
	cd doccoon_frontend && npm run dev

run-docker:
	docker-compose up --build
