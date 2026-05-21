# MCP Web Search

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ChenneyZhuang/mcp-web-search)](https://github.com/ChenneyZhuang/mcp-web-search/releases)

**Give your AI agent real-time web access. Zero API keys. Zero dependencies. ~30 KB.**

Search DuckDuckGo, extract page content, or do both in a single call — all through the Model Context Protocol. No signup, no billing, no limits beyond DuckDuckGo's soft rate throttling.

---

## Why This One?

| | This Server | `duckduckgo-mcp-server` | `ddg-search` |
|---|:---:|:---:|:---:|
| Runtime dependencies | **0** (stdlib only) | 3+ | 5+ |
| Python version | **3.9+** | 3.11+ | 3.10+ |
| Content extraction | ✅ | ✅ | ❌ |
| Batch extract (multiple URLs) | ✅ | ❌ | ❌ |
| Search + extract in one call | ✅ | ❌ | ❌ |
| Install size | ~30 KB | ~2 MB | ~1.5 MB |

Zero dependencies means zero supply-chain risk, instant install, and runs anywhere Python 3.9+ is available.

---

## Installation

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-web-search.git
```

That's it. No extra packages. No API keys.

### Docker

```bash
docker build -t mcp-web-search github.com/ChenneyZhuang/mcp-web-search
```

Or use the pre-built image:

```bash
docker run -i ghcr.io/chenneyzhuang/mcp-web-search:latest
```

---

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Cursor

Add to `.cursor/mcp.json`:

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

### Codex CLI

```bash
codex mcp add web-search -- python3 -m mcp_web_search.server
```

---

## Tools

### `web_search`

Search DuckDuckGo and return structured results.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | *(required)* | Search query |
| `limit` | `int` | `5` | Max results (1–20) |

**Returns:**

```json
[
  {
    "title": "Python (programming language) - Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)"
  }
]
```

### `web_extract`

Fetch and extract readable text from one or more web pages.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | `list[str]` | *(required)* | URLs to extract |

**Returns:**

```json
[
  {
    "url": "https://example.com",
    "content": "This domain is for use in illustrative examples...",
    "content_length": 1234
  }
]
```

Content is returned as plain text with HTML stripped. Capped at 5,000 characters per page. Results are cached to disk — the same URL extracted twice returns instantly.

### `web_search_and_extract`

Search AND extract page content in a single call. The most efficient workflow for agents that need both discovery and deep reading.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | *(required)* | Search query |
| `limit` | `int` | `3` | Max results to search and extract |

**Returns:** Same as `web_search`, plus a `content` field with extracted page text (capped at 3,000 chars).

---

## Usage Examples

### Basic research workflow

```
User: "What's new in Python 3.14?"
Agent: calls web_search("Python 3.14 new features", limit=5)
       → finds release notes URL
Agent: calls web_extract(["https://docs.python.org/3.14/whatsnew/3.14.html"])
       → extracts full page text
Agent: summarizes and answers
```

### One-shot lookup

```
User: "How do I set up Let's Encrypt on macOS?"
Agent: calls web_search_and_extract("Let's Encrypt macOS setup certbot", limit=3)
       → gets search results + full page text in one response
Agent: synthesizes answer from extracted docs
```

---

## How It Works

```
┌──────────┐     ┌─────────────┐     ┌──────────────┐
│ AI Agent │────▶│ MCP Protocol│────▶│ web_search() │
└──────────┘     └─────────────┘     └──────┬───────┘
                                            │
                                     ┌──────▼──────┐
                                     │ DuckDuckGo  │
                                     │ HTML Search │
                                     └──────┬──────┘
                                            │
                                     ┌──────▼──────┐
                                     │ Parse HTML  │
                                     │ → plain text│
                                     └─────────────┘
```

The server queries DuckDuckGo's HTML search endpoint (`html.duckduckgo.com`) — no API key, no JavaScript required. Results are parsed from the raw HTML and returned as structured objects. Content extraction uses regex-based HTML stripping — fast, dependency-free, and works on any page.

---

## Rate Limiting

DuckDuckGo imposes soft rate limits. For many requests in quick succession, add a 1–2 second delay between calls. The server does not auto-throttle — your agent is responsible for pacing.

For heavy usage, consider [DuckDuckGo's Instant Answer API](https://duckduckgo.com/api) or a paid search API.

---

## FAQ

**Does this use the official DuckDuckGo API?**
No. It parses the HTML search results page. Works without an API key but is subject to HTML structure changes.

**Is this legal?**
DuckDuckGo's robots.txt allows automated access at reasonable rates. Designed for AI agent research workflows, not high-volume scraping.

**What if a page blocks extraction?**
The server returns an error message like `[获取失败: HTTP 403]` — your agent should handle these gracefully.

**Can I use a proxy?**
Set `HTTP_PROXY` / `HTTPS_PROXY` environment variables — Python's `urllib` respects them automatically.

---

## Related

- [web-search](https://github.com/ChenneyZhuang/web-search) — the underlying zero-dependency search library (CLI + Python API)
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification

## License

MIT
