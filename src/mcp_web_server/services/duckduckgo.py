import logging
from typing import List, Dict, Any
from ddgs import DDGS
from datetime import datetime

logger = logging.getLogger(__name__)


class DuckDuckGoSearchService:
    """DuckDuckGo搜索服务"""

    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        执行DuckDuckGo搜索

        Args:
            query: 搜索关键词
            num_results: 返回结果数量，默认5条

        Returns:
            包含搜索结果的字典
        """
        if not query or not query.strip():
            return {
                "success": False,
                "error": "Search query cannot be empty",
                "results": [],
                "timestamp": datetime.now().isoformat()
            }

        num_results = min(max(1, num_results), 20)

        try:
            results = []
            for r in self.ddgs.text(query, max_results=num_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "description": r.get("body", "")
                })

            logger.info(f"Search completed for query: '{query}', found {len(results)} results")

            return {
                "success": True,
                "query": query,
                "num_results": len(results),
                "results": results,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Search error for query '{query}': {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "results": [],
                "timestamp": datetime.now().isoformat()
            }

    def news(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        执行DuckDuckGo新闻搜索

        Args:
            query: 搜索关键词
            num_results: 返回结果数量

        Returns:
            包含新闻搜索结果的字典
        """
        if not query or not query.strip():
            return {
                "success": False,
                "error": "Search query cannot be empty",
                "results": [],
                "timestamp": datetime.now().isoformat()
            }

        num_results = min(max(1, num_results), 20)

        try:
            results = []
            for r in self.ddgs.news(query, max_results=num_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "description": r.get("description", ""),
                    "date": r.get("date", "")
                })

            logger.info(f"News search completed for query: '{query}', found {len(results)} results")

            return {
                "success": True,
                "query": query,
                "num_results": len(results),
                "results": results,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"News search error for query '{query}': {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "results": [],
                "timestamp": datetime.now().isoformat()
            }


search_service = DuckDuckGoSearchService()
