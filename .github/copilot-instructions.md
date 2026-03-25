# Copilot project instructions

## 1) Project overview
- This repo is a FastMCP server implementation for Deutscher Wetterdienst (German Weather Service) in `main.py`.
- It uses `fastmcp.FastMCP` to create an MCP server that exposes weather-related tools.
- The server fetches data from DWD's public API endpoints and provides it via MCP tools.

## 2) Architecture and data flow (essential)
- `main.py` defines a FastMCP server instance `mcp = FastMCP("Deutscher Wetterdienst")`.
- Tools are registered using `@mcp.tool()` decorators (e.g., `get_weather_alerts`).
- Data flows: DWD API → `request_dwd_data()` → tool functions → MCP protocol.
- External API integration uses `httpx.AsyncClient` for HTTP requests to `https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/`.

## 3) Key patterns for AI edits
- Use `@mcp.tool(name, description)` decorator to register new tools.
- Follow async/await pattern for all API calls and tool implementations.
- Handle HTTP errors with try/except blocks and `response.raise_for_status()`.
- Use type hints (`from typing import Any`) for function parameters and return types.
- Include descriptive User-Agent headers for API requests.

## 4) Dependency and integration notes
- Core dependencies: `fastmcp`, `httpx` (async HTTP client).
- External API: Deutscher Wetterdienst public endpoints (no authentication required).
- Base URL is hardcoded: `dwd_base_url = "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/"`.
- Tools assume specific JSON endpoints exist on the DWD API.

## 5) Developer workflows
- Run locally: `python main.py` (executes the demo, calling `get_weather_alerts()` directly).
- For MCP server mode: Deploy via FastMCP server infrastructure (not implemented in this repo).
- Debugging: Use VS Code debugger or add print statements; API responses are printed to console.
- Testing: No test suite yet; add pytest tests in `tests/` for tool functions and API calls.

## 6) Project-specific conventions
- Tool functions return raw API data (dict/Any) without transformation.
- Error handling: Print errors to console and re-raise HTTP exceptions.
- Naming: Use descriptive tool names and English descriptions for international accessibility.
- Structure: Keep all logic in single `main.py` file; expand to modules only when complexity grows.

## 7) Action request to author
- Ask reviewer: "Should we add more weather-related tools (forecasts, station data) or focus on alerts only?"
- Ask reviewer: "Any plans for data caching, rate limiting, or error recovery mechanisms?"