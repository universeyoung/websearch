# MCP Web Server Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app

# 阿里云APT源
RUN sed -i "s@deb.debian.org@mirrors.aliyun.com@g" /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# 阿里云APT源 + 创建用户
RUN sed -i "s@deb.debian.org@mirrors.aliyun.com@g" /etc/apt/sources.list.d/debian.sources && \
    useradd -m mcpuser

COPY --from=builder /root/.local /home/mcpuser/.local

ENV PATH=/home/mcpuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

USER mcpuser

# ✅ 修复完成：用户组 + 空格
COPY --chown=mcpuser:mcpuser src/ ./src/

CMD ["python", "-m", "mcp_web_server.server"]
