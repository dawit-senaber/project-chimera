setup:
	uv sync

test:
	docker compose up --build --exit-code-from agent-chimera

spec-check:
	@echo "Checking for mandatory specification files..."
	@echo "Running spec-check script (validates skills against schemas)..."
	python -m scripts.spec_check

.PHONY: setup test spec-check