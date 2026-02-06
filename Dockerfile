# Use the official uv image for high-performance builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY . .

# Install dependencies using the lockfile
RUN uv sync --frozen

# Install lightweight dev/test DB driver so integration tests can run inside container
RUN python -m pip install --upgrade pip && python -m pip install psycopg2-binary pytest

# Command to run tests inside the container
CMD ["uv", "run", "pytest"]