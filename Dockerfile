# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv using the official method (copy from official uv image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock* ./
COPY requirements.txt ./

# Install Python dependencies using uv
RUN uv sync

# Copy application code
COPY . .

# Create directory for session files
RUN mkdir -p /app/sessions

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check - test if the bot can run
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD uv run python health_check.py || exit 1

# Default command: run the scheduler
CMD ["uv", "run", "python", "main.py"]
