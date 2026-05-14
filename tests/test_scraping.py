import pytest
from unittest.mock import AsyncMock, patch
from mcp.types import TextContent
from mcp_web_server.tools.scraping import handle_web_scrape, handle_web_scrape_batch


class TestWebScraping:
    """Test cases for web scraping tools"""

    @pytest.mark.asyncio
    async def test_handle_web_scrape_invalid_args(self):
        """Test scrape with invalid arguments"""
        result = await handle_web_scrape({"url": 123})
        assert len(result) == 1
        assert "Invalid arguments" in result[0].text

    @pytest.mark.asyncio
    @patch('mcp_web_server.tools.scraping.httpx.AsyncClient')
    async def test_handle_web_scrape_success(self, mock_client):
        """Test successful web scraping"""
        mock_response = AsyncMock()
        mock_response.text = "<html><head><title>Test Page</title></head><body><p>Hello World</p></body></html>"
        mock_response.raise_for_status = MagicMock()

        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = await handle_web_scrape({"url": "https://example.com"})

        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "example.com" in result[0].text
        assert "Test Page" in result[0].text

    @pytest.mark.asyncio
    async def test_handle_web_scrape_batch_invalid_args(self):
        """Test batch scrape with invalid arguments"""
        result = await handle_web_scrape_batch({})
        assert len(result) == 1
        assert "Invalid arguments" in result[0].text

    @pytest.mark.asyncio
    async def test_handle_web_scrape_batch_too_many_urls(self):
        """Test batch scrape with too many URLs"""
        urls = [f"https://example{i}.com" for i in range(15)]
        result = await handle_web_scrape_batch({"urls": urls})
        assert len(result) == 1
        assert "Maximum 10 URLs" in result[0].text


class TestScrapeURL:
    """Test cases for scrape_url function"""

    @pytest.mark.asyncio
    @patch('mcp_web_server.tools.scraping.httpx.AsyncClient')
    async def test_scrape_url_removes_scripts(self, mock_client):
        """Test that script tags are removed from content"""
        html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <script>alert('test');</script>
            <p>Main content</p>
        </body>
        </html>
        """
        mock_response = AsyncMock()
        mock_response.text = html
        mock_response.raise_for_status = MagicMock()

        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value.get.return_value = mock_response
        mock_client.return_value = mock_instance

        from mcp_web_server.tools.scraping import scrape_url
        result = await scrape_url("https://example.com")

        assert result["success"] is True
        assert "alert" not in result["content"]
        assert "Main content" in result["content"]

    @pytest.mark.asyncio
    @patch('mcp_web_server.tools.scraping.httpx.AsyncClient')
    async def test_scrape_url_respects_max_length(self, mock_client):
        """Test that content respects max_length limit"""
        html = "<html><body><p>" + "a" * 10000 + "</p></body></html>"
        mock_response = AsyncMock()
        mock_response.text = html
        mock_response.raise_for_status = MagicMock()

        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value.get.return_value = mock_response
        mock_client.return_value = mock_instance

        from mcp_web_server.tools.scraping import scrape_url
        result = await scrape_url("https://example.com", max_length=100)

        assert result["success"] is True
        assert len(result["content"]) <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
