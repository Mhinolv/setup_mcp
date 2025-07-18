# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy dependency files and resource first for better caching
COPY pyproject.toml uv.lock SETUP.md ./

# Install dependencies with uv
RUN uv sync --frozen

# Copy the rest of the project files
COPY . .

# Use a non-root user for security (optional, can be commented out if issues)
RUN useradd -m mcpuser && chown -R mcpuser /app
USER mcpuser

# Expose no ports (stdio transport by default)

# Default command: run the MCP server using uv
CMD ["uv", "run", "python", "main.py"] 