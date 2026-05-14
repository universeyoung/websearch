# MCP Web Server 最终版Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

RUN useradd -m mcpuser
COPY --from=builder /root/.local /home/mcpuser/.local

ENV PATH=/home/mcpuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

USER mcpuser
COPY --chown=mcpuser:mcpuser src/ ./src/

CMD ["python", "-m", "mcp_web_server.server"]