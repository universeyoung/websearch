import logging
from typing import Any
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from mcp_web_server.services.duckduckgo import search_service

logger = logging.getLogger(__name__)


class WebSearchInput(BaseModel):
    """Web search input schema"""
    query: str = Field(description="Search query string")
    num_results: int = Field(default=5, description="Number of results to return (1-20)", ge=1, le=20)


class WebSearchNewsInput(BaseModel):
    """Web news search input schema"""
    query: str = Field(description="Search query string for news")
    num_results: int = Field(default=5, description="Number of results to return (1-20)", ge=1, le=20)


async def handle_web_search(arguments: Any) -> list[TextContent]:
    """
    Handle web search requests

    Args:
        arguments: Tool arguments

    Returns:
        List of text content results
    """
    try:
        args = WebSearchInput(**arguments) if isinstance(arguments, dict) else WebSearchInput(**arguments)
    except Exception as e:
        return [TextContent(type="text", text=f"Invalid arguments: {e}")]

    result = search_service.search(args.query, args.num_results)

    if result["success"]:
        output = f"Search Results for '{result['query']}'\n\n"
        for i, item in enumerate(result["results"], 1):
            output += f"{i}. {item['title']}\n"
            output += f"   URL: {item['url']}\n"
            output += f"   {item['description']}\n\n"
        output += f"Found {result['num_results']} results. Timestamp: {result['timestamp']}"
    else:
        output = f"Search failed: {result.get('error', 'Unknown error')}"

    return [TextContent(type="text", text=output)]


async def handle_web_search_news(arguments: Any) -> list[TextContent]:
    """
    Handle web news search requests

    Args:
        arguments: Tool arguments

    Returns:
        List of text content results
    """
    try:
        args = WebSearchNewsInput(**arguments) if isinstance(arguments, dict) else WebSearchNewsInput(**arguments)
    except Exception as e:
        return [TextContent(type="text", text=f"Invalid arguments: {e}")]

    result = search_service.news(args.query, args.num_results)

    if result["success"]:
        output = f"News Results for '{result['query']}'\n\n"
        for i, item in enumerate(result["results"], 1):
            output += f"{i}. {item['title']}\n"
            output += f"   URL: {item['url']}\n"
            output += f"   Date: {item.get('date', 'N/A')}\n"
            output += f"   {item['description']}\n\n"
        output += f"Found {result['num_results']} news results. Timestamp: {result['timestamp']}"
    else:
        output = f"News search failed: {result.get('error', 'Unknown error')}"

    return [TextContent(type="text", text=output)]


web_search = Tool(
    name="web_search",
    description="Search the web using DuckDuckGo. Returns web search results with titles, URLs, and descriptions.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query string"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return (1-20)",
                "default": 5,
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["query"]
    }
)

web_search_news = Tool(
    name="web_search_news",
    description="Search for news using DuckDuckGo. Returns news articles with titles, URLs, dates, and descriptions.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "News search query string"
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return (1-20)",
                "default": 5,
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["query"]
    }
)
