# Dockerfile for MCPServer FastMCP weather service

FROM python:3.12-slim

WORKDIR /app

# Copy application code
COPY main.py /app/main.py
COPY .github/copilot-instructions.md /app/.github/copilot-instructions.md

# Install runtime dependencies
RUN pip install --no-cache-dir fastmcp httpx

# Default command to run the service
CMD ["python", "main.py"]
