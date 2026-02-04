setup:
	uv sync

test:
	docker compose up --build --exit-code-from agent-chimera

spec-check:
	@echo "Checking for mandatory specification files..."
	@test -d specs || (echo "Error: specs directory missing"; exit 1)
	@test -f specs/technical.md || (echo "Error: technical.md missing"; exit 1)
	@echo "All specs present."