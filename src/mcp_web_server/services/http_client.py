import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)


class HTTPClientService:
    """HTTP客户端服务"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        """获取或创建HTTP客户端"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
            )
        return self._client

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """发送GET请求"""
        client = await self.get_client()
        try:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.TimeoutException:
            logger.error(f"Request timeout for URL: {url}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP error for URL {url}: {e}")
            raise

    async def close(self):
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None


http_client_service = HTTPClientService()
