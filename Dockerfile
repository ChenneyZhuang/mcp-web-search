FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir git+https://github.com/ChenneyZhuang/mcp-web-search.git

ENTRYPOINT ["python3", "-m", "mcp_web_search.server"]
