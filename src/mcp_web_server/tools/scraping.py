import logging
from typing import Any, List
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from mcp_web_server.services.http_client import http_client_service
from bs4 import BeautifulSoup
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class WebScrapeInput(BaseModel):
    """Web scrape input schema"""
    url: str = Field(description="URL of the webpage to scrape")
    max_length: int = Field(default=5000, description="Maximum number of characters to return", ge=100, le=50000)


class WebScrapeBatchInput(BaseModel):
    """Batch web scrape input schema"""
    urls: List[str] = Field(description="List of URLs to scrape (max 10)")
    max_length: int = Field(default=3000, description="Maximum number of characters per page", ge=100, le=50000)


async def scrape_url(url: str, max_length: int = 5000) -> dict:
    """
    Scrape a single URL

    Args:
        url: Target URL
        max_length: Maximum characters to return

    Returns:
        Scraping result dictionary
    """
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')

            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            title = soup.title.string if soup.title else ""

            text = soup.get_text(separator='\n', strip=True)
            lines = [line for line in text.split('\n') if line.strip()]
            text = '\n'.join(lines)
            text = text[:max_length]

            return {
                "success": True,
                "url": url,
                "title": title.strip() if title else "",
                "content": text,
                "timestamp": datetime.now().isoformat()
            }

    except httpx.TimeoutException:
        logger.error(f"Timeout scraping URL: {url}")
        return {
            "success": False,
            "url": url,
            "error": "Request timeout"
        }
    except httpx.HTTPError as e:
        logger.error(f"HTTP error scraping {url}: {e}")
        return {
            "success": False,
            "url": url,
            "error": f"HTTP error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


async def handle_web_scrape(arguments: Any) -> list[TextContent]:
    """
    Handle web scrape requests

    Args:
        arguments: Tool arguments

    Returns:
        List of text content results
    """
    try:
        args = WebScrapeInput(**arguments) if isinstance(arguments, dict) else WebScrapeInput(**arguments)
    except Exception as e:
        return [TextContent(type="text", text=f"Invalid arguments: {e}")]

    result = await scrape_url(args.url, args.max_length)

    if result["success"]:
        output = f"Scraped: {result['url']}\n"
        output += f"Title: {result['title']}\n\n"
        output += f"Content:\n{result['content']}\n\n"
        output += f"Timestamp: {result['timestamp']}"
    else:
        output = f"Failed to scrape {result['url']}: {result.get('error', 'Unknown error')}"

    return [TextContent(type="text", text=output)]


async def handle_web_scrape_batch(arguments: Any) -> list[TextContent]:
    """
    Handle batch web scrape requests

    Args:
        arguments: Tool arguments

    Returns:
        List of text content results
    """
    try:
        args = WebScrapeBatchInput(**arguments) if isinstance(arguments, dict) else WebScrapeBatchInput(**arguments)
    except Exception as e:
        return [TextContent(type="text", text=f"Invalid arguments: {e}")]

    if len(args.urls) > 10:
        return [TextContent(type="text", text="Maximum 10 URLs allowed per batch request")]

    results = []
    for url in args.urls:
        result = await scrape_url(url, args.max_length)
        results.append(result)

    output = f"Batch Scrape Results ({len(results)} pages)\n\n"
    for i, result in enumerate(results, 1):
        if result["success"]:
            output += f"{i}. {result['url']}\n"
            output += f"   Title: {result['title']}\n"
            output += f"   Content preview: {result['content'][:200]}...\n\n"
        else:
            output += f"{i}. {result['url']}\n"
            output += f"   ERROR: {result.get('error', 'Unknown error')}\n\n"

    return [TextContent(type="text", text=output)]


web_scrape = Tool(
    name="web_scrape",
    description="Scrape content from a webpage. Returns the page title and main text content.",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL of the webpage to scrape"
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum number of characters to return",
                "default": 5000,
                "minimum": 100,
                "maximum": 50000
            }
        },
        "required": ["url"]
    }
)

web_scrape_batch = Tool(
    name="web_scrape_batch",
    description="Scrape content from multiple webpages at once. Returns titles and main text content for each page.",
    inputSchema={
        "type": "object",
        "properties": {
            "urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of URLs to scrape (max 10)"
            },
            "max_length": {
                "type": "integer",
                "description": "Maximum number of characters per page",
                "default": 3000,
                "minimum": 100,
                "maximum": 50000
            }
        },
        "required": ["urls"]
    }
)
