# MCP Web Search

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-web-search/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ChenneyZhuang/mcp-web-search)](https://github.com/ChenneyZhuang/mcp-web-search/releases)

**The lightest MCP web search server in the ecosystem.**
Zero runtime dependencies beyond Python stdlib. No API key. No account.
Your AI agent gets real-time web access in one command.

---

## Table of Contents

- [Why This One?](#why-this-one)
- [Installation](#installation)
- [Configuration](#configuration)
- [Tools](#tools)
  - [web_search](#web_search)
  - [web_extract](#web_extract)
  - [web_search_and_extract](#web_search_and_extract)
- [Usage Examples](#usage-examples)
- [How It Works](#how-it-works)
- [Rate Limiting](#rate-limiting)
- [FAQ](#faq)
- [Related](#related)
- [License](#license)

---

## Why This One?

There are several DuckDuckGo MCP servers. Here's why this one stands out:

| | This Server | `duckduckgo-mcp-server` | `ddg-search` |
|---|---|:---:|:---:|
| Runtime dependencies | **0** (stdlib only) | 3+ | 5+ |
| Python version | **3.9+** | 3.11+ | 3.10+ |
| Content extraction | ✅ markdown | ✅ plain text | ❌ |
| Batch extract (multiple URLs) | ✅ | ❌ | ❌ |
| Search + extract combo | ✅ single call | ❌ | ❌ |
| Install size | ~30 KB | ~2 MB | ~1.5 MB |

Zero dependencies means zero supply-chain risk, zero version conflicts, and
instant installation on any machine with Python 3.9+.

---

## Installation

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-web-search.git
```

No extra packages. No API keys. Works immediately.

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

**Parameters:**
- `query` (str) — search query
- `limit` (int, default 5) — max results (1–20)

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

Fetch and extract readable text from web pages. Ideal for reading documentation,
articles, or any page found via `web_search`.

**Parameters:**
- `urls` (list[str]) — one or more URLs to extract

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

Content is returned as **plain text** with HTML tags stripped.

### `web_search_and_extract`

Search AND extract full page content in a single call. The most efficient
workflow for AI agents that need both discovery and deep reading.

**Parameters:**
- `query` (str) — search query
- `limit` (int, default 3) — max results to search AND extract

**Returns:** Same as `web_search`, plus a `content` field with extracted page text.

---

## Usage Examples

### Basic research workflow

```
User: "What's new in Python 3.14?"
Agent: calls web_search("Python 3.14 new features", limit=5)
       → finds release notes URL
Agent: calls web_extract(["https://docs.python.org/3.14/whatsnew/3.14.html"])
       → extracts full changelog as markdown
Agent: summarizes and answers
```

### One-shot lookup

```
User: "How do I set up Let's Encrypt on macOS?"
Agent: calls web_search_and_extract("Let's Encrypt macOS setup certbot", limit=3)
       → gets search results + extracted content in one response
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
                                     │ Parse + fmt │
                                     │ → markdown  │
                                     └─────────────┘
```

The server uses DuckDuckGo's HTML search endpoint (no API key, no JavaScript
required). Results are parsed from the HTML response and formatted as structured
objects. Content extraction uses regex-based HTML parsing — fast and dependency-free.

---

## Rate Limiting

DuckDuckGo imposes soft rate limits. If you're making many requests in quick
succession, add a 1–2 second delay between calls. The server does not
auto-throttle — your agent is responsible for pacing.

For heavy usage, consider DuckDuckGo's [Instant Answer API](https://duckduckgo.com/api)
(rate-limited but documented) or a paid search API.

---

## FAQ

**Does this use the official DuckDuckGo API?**
No. It parses the HTML search results page, similar to how a browser would
render them. This means it works without an API key but is subject to HTML
structure changes.

**Is this legal?**
DuckDuckGo's robots.txt allows automated access at reasonable rates.
This server is designed for AI agent research workflows, not high-volume
scraping. Respect the service.

**What if a page blocks extraction?**
Some sites block automated access. The server returns `[获取失败: HTTP 403]`
or similar error messages. Your agent should handle these gracefully.

**Can I use a proxy?**
Not built-in. If you need proxy support, set the `HTTP_PROXY` / `HTTPS_PROXY`
environment variables — Python's `urllib` respects them automatically.

---

## Related

- [web-search](https://github.com/ChenneyZhuang/web-search) — the underlying zero-dependency search library
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification
- [duckduckgo-mcp-server](https://github.com/nickclyde/duckduckgo-mcp-server) — alternative with more features but heavier dependencies

## License

MIT
