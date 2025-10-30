# Zero API Key MCP-servers

This repository contains a collection of small, zero-API-key FastMCP servers intended for everyday use with a local LLM (e.g. LMStudio or Ollama).

## What’s included

- Ping server
    - Simple internet/connectivity check (checking if gooogle.com is pingable).
- Weather server (German forecasts)
    - Checks the German Weather Service data via the Brightsky API.
    - Tools:
        - Current weather
        - Get location info (station, location data)
        - Weather forecast
- Wikipedia server
    - Queries /wikipedia?query=<search terms> and pulls the info header (the part that is also shown on Google preview)
- General web-search server
    - Queries brave.com/search?q=<query>
    - Scrapes the Brave Search to fetch results.
    - Deep search capability to follow and extract content from top search results for more thorough responses.

## Quick start

1. Clone the repository
2. `uv sync`
3. copy-paste `mcp.json` config into your IDEs `mcp.json`
4. enjoy
