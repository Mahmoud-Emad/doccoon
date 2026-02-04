.PHONY: help run-backend run-frontend run-docker deploy stop logs

help:
	@echo "Doccoon - Available commands:"
	@echo ""
	@echo "  make run-backend    Start the Django backend server (dev)"
	@echo "  make run-frontend   Start the Vue.js frontend dev server (dev)"
	@echo "  make run-docker     Build and start all services with Docker"
	@echo "  make deploy         Full deployment with auto-fix for Docker issues"
	@echo "  make stop           Stop all Docker services"
	@echo "  make logs           View Docker logs"
	@echo "  make help           Show this help message"

run-backend:
	cd doccoon_backend && uv run python manage.py runserver

run-frontend:
	cd doccoon_frontend && npm run dev

run-docker:
	docker compose up --build

deploy:
	./deploy.sh

stop:
	docker compose down

logs:
	docker compose logs -f
