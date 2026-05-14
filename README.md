# MCP Web Server

A Model Context Protocol (MCP) server that provides web search and web scraping capabilities. Designed for deployment on cloud servers using Docker.

## Features

- **Web Search**: Search the web using DuckDuckGo API
- **News Search**: Search for news articles
- **Web Scraping**: Extract content from webpages
- **Batch Scraping**: Scrape multiple URLs at once
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-web-server
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python -m mcp_web_server.server
```

### Option 2: Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. Check the status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_HOST` | Host to bind to | `0.0.0.0` |
| `MCP_PORT` | Port to listen on | `3000` |
| `PYTHONUNBUFFERED` | Enable unbuffered output | `1` |

### Docker Resource Limits

The Docker Compose configuration includes resource limits:
- CPU: 0.5 cores
- Memory: 256MB
- Log rotation: 10MB max, 3 files

## Available Tools

### web_search

Search the web using DuckDuckGo.

**Parameters:**
- `query` (string, required): Search query
- `num_results` (integer, optional): Number of results (1-20, default: 5)

**Example:**
```json
{
  "query": "Python programming",
  "num_results": 10
}
```

### web_search_news

Search for news articles.

**Parameters:**
- `query` (string, required): News search query
- `num_results` (integer, optional): Number of results (1-20, default: 5)

### web_scrape

Extract content from a webpage.

**Parameters:**
- `url` (string, required): Target URL
- `max_length` (integer, optional): Maximum characters (100-50000, default: 5000)

**Example:**
```json
{
  "url": "https://example.com",
  "max_length": 3000
}
```

### web_scrape_batch

Extract content from multiple webpages.

**Parameters:**
- `urls` (array, required): List of URLs (max 10)
- `max_length` (integer, optional): Maximum characters per page (default: 3000)

**Example:**
```json
{
  "urls": ["https://example.com", "https://example.org"],
  "max_length": 3000
}
```

## Usage with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "web-search": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp-web-server"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "web-search": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "mcp-web-server"]
    }
  }
}
```

### Direct Connection

For local development:
```bash
# Build the Docker image
docker build -t mcp-web-server .

# Run in interactive mode
docker run --rm -i mcp-web-server
```

## Cloud Deployment

### AWS (EC2)

1. Launch an EC2 instance (t2.micro or larger)
2. Install Docker:
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker ubuntu
```

3. Transfer project files and start:
```bash
docker-compose up -d
```

4. Configure security group to allow port 3000 if needed

### Google Cloud Platform

1. Create a VM instance with Container-Optimized OS
2. Install Docker Compose:
```bash
sudo apt install docker-compose
```

3. Deploy:
```bash
docker-compose up -d
```

### DigitalOcean

1. Create a droplet with Docker pre-installed
2. Clone repository and deploy:
```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

**Connection refused:**
- Check if the container is running: `docker-compose ps`
- Check logs: `docker-compose logs`

**Search returns no results:**
- Check network connectivity from container
- Verify DuckDuckGo is accessible

**Scraping timeout:**
- Increase timeout in code
- Check target website availability

### Logs

View real-time logs:
```bash
docker-compose logs -f --tail=100
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Project Structure

```
mcp-web-server/
├── src/
│   └── mcp_web_server/
│       ├── server.py           # Main server entry
│       ├── tools/
│       │   ├── search.py       # Search tool implementations
│       │   └── scraping.py     # Scraping tool implementations
│       └── services/
│           ├── duckduckgo.py    # DuckDuckGo API service
│           └── http_client.py   # HTTP client service
├── tests/                      # Unit tests
├── docker/
│   └── Dockerfile             # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── requirements.txt           # Python dependencies
└── pyproject.toml            # Project metadata
```

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
