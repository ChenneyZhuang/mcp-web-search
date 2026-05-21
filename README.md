# 🔍 MCP Web Search

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)]()
[![CI](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml)

**MCP server for DuckDuckGo web search. Zero dependencies. No API key required.**

The lightest web search MCP server in the ecosystem — your AI agent gets
real-time web access in one command.

---

## Quick Start

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-web-search.git
```

### Claude Desktop

```json
{
  "mcpServers": {
    "web-search": {
      "command": "python3",
      "args": ["-m", "mcp_web_search.server"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add web-search python3 -m mcp_web_search.server
```

---

## Tools

| Tool | Description |
|------|-------------|
| `web_search(query, limit=5)` | Search DuckDuckGo |
| `web_extract(urls)` | Extract readable text from pages |
| `web_search_and_extract(query, limit=3)` | Search + extract in one call |

---

## Why This One?

| | This Server | `duckduckgo-mcp-server` |
|---|:--:|:--:|
| Dependencies | **0** | 3+ |
| Python version | **3.9+** | 3.11+ |
| Content extraction | ✅ | ✅ |
| Batch extract | ✅ | ❌ |
| Search + extract combo | ✅ | ❌ |

---

## License

MIT
