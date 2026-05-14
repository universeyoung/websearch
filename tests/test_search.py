import pytest
from unittest.mock import patch, MagicMock
from mcp_web_server.services.duckduckgo import DuckDuckGoSearchService


class TestDuckDuckGoSearchService:
    """Test cases for DuckDuckGo search service"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = DuckDuckGoSearchService()

    def test_search_empty_query(self):
        """Test search with empty query"""
        result = self.service.search("")
        assert result["success"] is False
        assert "empty" in result["error"].lower()

    def test_search_whitespace_query(self):
        """Test search with whitespace query"""
        result = self.service.search("   ")
        assert result["success"] is False

    @patch('mcp_web_server.services.duckduckgo.DDGS')
    def test_search_success(self, mock_ddgs):
        """Test successful search"""
        mock_instance = MagicMock()
        mock_instance.text.return_value = iter([
            {"title": "Test Result", "href": "https://example.com", "body": "Description"}
        ])
        mock_ddgs.return_value = mock_instance

        service = DuckDuckGoSearchService()
        result = service.search("test query", num_results=5)

        assert result["success"] is True
        assert result["query"] == "test query"
        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "Test Result"

    @patch('mcp_web_server.services.duckduckgo.DDGS')
    def test_search_num_results_limit(self, mock_ddgs):
        """Test that num_results is capped at 20"""
        mock_instance = MagicMock()
        mock_instance.text.return_value = iter([])
        mock_ddgs.return_value = mock_instance

        service = DuckDuckGoSearchService()
        result = service.search("test", num_results=100)

        assert result["success"] is True

    @patch('mcp_web_server.services.duckduckgo.DDGS')
    def test_news_search_success(self, mock_ddgs):
        """Test successful news search"""
        mock_instance = MagicMock()
        mock_instance.news.return_value = iter([
            {"title": "News Article", "url": "https://news.com", "description": "News desc", "date": "2024-01-01"}
        ])
        mock_ddgs.return_value = mock_instance

        service = DuckDuckGoSearchService()
        result = service.news("test news", num_results=5)

        assert result["success"] is True
        assert len(result["results"]) == 1
        assert "date" in result["results"][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
