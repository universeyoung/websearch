# MCP Web Search & Scraping Server - 技术规格说明

## 1. 项目概述

**项目名称**: mcp-web-server
**项目类型**: Model Context Protocol (MCP) 服务器
**核心功能**: 提供联网搜索和网页内容抓取的MCP工具，支持Docker云服务器部署
**目标用户**: AI应用开发者，需要让大语言模型访问互联网资源的用户

## 2. 功能规格

### 2.1 核心功能

#### Web Search (网络搜索)
- **工具名称**: `web_search`
- **功能**: 使用搜索引擎API进行网络搜索
- **参数**:
  - `query` (必需): 搜索关键词字符串
  - `num_results` (可选): 返回结果数量，默认5条，最大20条
- **返回数据**:
  - 搜索结果列表，包含标题、URL、摘要
  - 搜索时间戳
- **API选择**: 使用 DuckDuckGo API (免费，无需API Key)

#### Web Scraping (网页抓取)
- **工具名称**: `web_scrape`
- **功能**: 抓取指定网页的文本内容
- **参数**:
  - `url` (必需): 目标网页URL
  - `max_length` (可选): 最大抓取字符数，默认5000
- **返回数据**:
  - 网页标题
  - 网页主要内容（去除HTML标签）
  - 提取时间戳

#### Batch Web Scraping (批量网页抓取)
- **工具名称**: `web_scrape_batch`
- **功能**: 批量抓取多个网页内容
- **参数**:
  - `urls` (必需): URL数组，最多10个
  - `max_length` (可选): 每个网页最大字符数，默认3000
- **返回数据**:
  - 每个URL对应的抓取结果

### 2.2 技术架构

```
┌─────────────────────────────────────────────────────┐
│           MCP Client (Claude Desktop等)             │
└──────────────────┬──────────────────────────────────┘
                   │ JSON-RPC 2.0 over stdio
┌──────────────────▼──────────────────────────────────┐
│              MCP Web Server                          │
│  ┌──────────────────────────────────────────────┐   │
│  │  Protocol Layer (mcp-core)                   │   │
│  └─────────────────┬────────────────────────────┘   │
│  ┌─────────────────▼────────────────────────────┐   │
│  │  Tools Layer                                  │   │
│  │  - web_search                                 │   │
│  │  - web_scrape                                 │   │
│  │  - web_scrape_batch                           │   │
│  └─────────────────┬────────────────────────────┘   │
│  ┌─────────────────▼────────────────────────────┐   │
│  │  Services Layer                               │   │
│  │  - SearchService (DuckDuckGo)                 │   │
│  │  - ScrapingService (HTTP + BeautifulSoup)    │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 2.3 技术栈

- **语言**: Python 3.11+
- **MCP SDK**: mcp (官方Python SDK)
- **Web Scraping**: requests, beautifulsoup4
- **搜索API**: DuckDuckGo (无需API Key)
- **容器化**: Docker, Docker Compose
- **异步处理**: asyncio

### 2.4 项目结构

```
mcp-web-server/
├── src/
│   └── mcp_web_server/
│       ├── __init__.py
│       ├── server.py              # MCP服务器主入口
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── search.py          # 搜索工具实现
│       │   └── scraping.py        # 抓取工具实现
│       └── services/
│           ├── __init__.py
│           ├── duckduckgo.py      # DuckDuckGo搜索服务
│           └── http_client.py     # HTTP客户端服务
├── tests/
│   ├── __init__.py
│   ├── test_search.py
│   └── test_scraping.py
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── SPEC.md
└── README.md
```

### 2.5 Docker配置要求

- **基础镜像**: python:3.11-slim
- **优化**:
  - 多阶段构建减小镜像体积
  - 非root用户运行提高安全性
  - 健康检查配置
- **环境变量**:
  - `MCP_HOST`: 绑定地址，默认0.0.0.0
  - `MCP_PORT`: 端口，默认3000（虽然stdio模式不使用）
- **资源限制**:
  - 内存: 256MB
  - CPU: 0.5

### 2.6 错误处理

- 网络超时: 返回超时错误信息
- 解析失败: 返回部分数据和错误提示
- 无结果: 返回空列表和提示
- 格式错误: 返回参数错误信息

## 3. 验收标准

### 3.1 功能验收

- [ ] MCP服务器能正常启动并暴露3个工具
- [ ] web_search能返回搜索结果
- [ ] web_scrape能抓取网页内容
- [ ] web_scrape_batch能批量抓取多个网页
- [ ] Docker容器能成功构建和运行
- [ ] Docker Compose能一键部署

### 3.2 质量标准

- [ ] 所有代码通过基础语法检查
- [ ] 包含单元测试
- [ ] 错误处理完善
- [ ] 日志记录清晰
- [ ] README文档完整

### 3.3 部署验收

- [ ] Docker镜像构建成功
- [ ] 容器能正常启动
- [ ] MCP客户端能连接并调用工具
- [ ] 云服务器部署说明清晰
