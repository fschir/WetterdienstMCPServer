"""
FastMCP server for Deutscher Wetterdienst (German Weather Service).

This server provides weather-related tools using the FastMCP framework,
fetching data from the DWD's public API endpoints.
"""

import asyncio
import httpx
import argparse
from fastmcp import FastMCP
from typing import Any



mcp = FastMCP("Deutscher Wetterdienst")

dwd_base_url = "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/"

async def request_dwd_data(endpoint: str, additional_headers: dict = None, params:dict = None) -> Any:
    """
    Fetch data from the Deutscher Wetterdienst API.

    Args:
        endpoint: The API endpoint path to request (relative to dwd_base_url)
        additional_headers: Optional dictionary of additional HTTP headers to include in the request
        params: Optional dictionary of query parameters for the request

    Returns:
        The JSON response data from the API

    Raises:
        httpx.HTTPError: If the HTTP request fails
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    if additional_headers:
        headers = headers | additional_headers
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{dwd_base_url}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching DWD data from {endpoint}: {e}")
            raise   

@mcp.tool(name="get_weather_alerts", description="Get current weather alerts from the Deutscher Wetterdienst.")
async def get_weather_alerts() -> Any:
    """
    Retrieve current weather alerts from the Deutscher Wetterdienst.

    Fetches the latest weather warnings and alerts in English from the DWD API.

    Returns:
        Dictionary containing weather alert data
    """
    alert_url = "warnings_nowcast_en.json"
    data = await request_dwd_data(alert_url)
    if not data:
        return {"No weather alerts found."}
    else:
        print(data)
        return data

@mcp.tool(name="get_weather_from_station", description="Get current weather data from specific weather stations by their IDs.")
async def get_weather_from_station(ids: list[str]) -> Any:
    """
    Fetches current weather data from specific weather stations by their IDs.
    Args:
        ids: A list of station IDs to fetch weather data for.    
    """
    station_url = f"stationOverviewExtended"
    if not ids:
        return {"No station IDs provided."}
    data = await request_dwd_data(station_url, params={"stationIds": ids})
    if not data:
        return {"No weather data found for the provided station IDs."}
    else:
        return data





def main():
    """
    Main entry point for running the weather alerts tool.

    This function starts the FastMCP server, making the weather alerts tool available for use.
    """

    parser = argparse.ArgumentParser(description="Run the Deutscher Wetterdienst FastMCP server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP to bind the HTTP server")
    parser.add_argument("--port", type=int, default=8823, help="Port number for the HTTP server")
    args = parser.parse_args()

    mcp.run(transport="http", host=args.host, port=args.port)

if __name__ == "__main__":
    main()