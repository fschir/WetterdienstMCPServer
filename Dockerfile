# Dockerfile for MCPServer FastMCP weather service

FROM python:3.12-slim

WORKDIR ${INSTALL_PATH:-.}/app

# Copy application code
COPY main.py ${INSTALL_PATH:-.}/app/main.py
COPY ${INSTALL_PATH:-.}/.github/copilot-instructions.md ${INSTALL_PATH:-.}/app/.github/copilot-instructions.md

# Install runtime dependencies
RUN pip install --no-cache-dir fastmcp httpx

# Default command to run the service
CMD ["python", "main.py"]
