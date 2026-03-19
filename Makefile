.PHONY: help run stop test seed

BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

help:
	@echo "$(BLUE)Доступные команды:$(RESET)"
	@awk 'BEGIN {FS = ":.*##"; printf "\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

run:
	@echo "$(YELLOW)Запуск контейнеров...$(RESET)"
	docker-compose up -d
	@echo "$(GREEN)Проект запущен!$(RESET)"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"

stop:
	@echo "$(YELLOW)Остановка контейнеров...$(RESET)"
	docker-compose down
	@echo "$(GREEN)Проект остановлен!$(RESET)"

test:
	@echo "$(YELLOW)Запуск юнит-тестов...$(RESET)"
	docker-compose exec user-activity-api pytest -v app/tests/test_analytics.py

seed:
	@echo "$(YELLOW)Заполнение тестовыми данными...$(RESET)"
	docker-compose exec user-activity-api python -m app.database.seed_data
