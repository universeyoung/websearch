import asyncio
import logging
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mcp_web_server.tools.search import web_search, web_search_news, handle_web_search, handle_web_search_news
from mcp_web_server.tools.scraping import web_scrape, web_scrape_batch, handle_web_scrape, handle_web_scrape_batch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

server = Server("mcp-web-server")

TOOL_HANDLERS = {
    "web_search": handle_web_search,
    "web_search_news": handle_web_search_news,
    "web_scrape": handle_web_scrape,
    "web_scrape_batch": handle_web_scrape_batch,
}


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [web_search, web_search_news, web_scrape, web_scrape_batch]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from MCP clients"""
    logger.info(f"Tool call received: {name} with arguments: {arguments}")

    handler = TOOL_HANDLERS.get(name)
    if not handler:
        logger.error(f"Unknown tool: {name}")
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    try:
        result = await handler(arguments)
        logger.info(f"Tool {name} executed successfully")
        return result
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting MCP Web Server...")

    try:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
