SCRIPTS_DIR := scripts
CREATE_ENV := $(SCRIPTS_DIR)/init.sh
ENV_FILE := .env
TEST_DIR := tests

.PHONY: init reinit clean test

init:
	@if [ -f $(ENV_FILE) ]; then \
		echo "$(ENV_FILE) already exists. Skipping initialization."; \
		echo "If you want to recreate it, run 'make reinit'."; \
	else \
		bash $(CREATE_ENV); \
	fi

reinit:
	@rm -f $(ENV_FILE)
	@$(MAKE) init

clean:
	@rm -f $(ENV_FILE)
	@echo "🧹 Cleaned .env file"

test:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "No $(ENV_FILE) found. Run 'make init' first."; \
		exit 1; \
	fi
	@echo "Running tests..."
	@uv run pytest $(TEST_DIR) -v
