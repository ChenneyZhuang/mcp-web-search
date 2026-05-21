"""MCP server for DuckDuckGo web search."""

from mcp.server.fastmcp import FastMCP
from websearch import search, extract, search_and_extract

mcp = FastMCP("Web Search")


@mcp.tool()
def web_search(query: str, limit: int = 5) -> list[dict]:
    """Search the web via DuckDuckGo. Returns titles and URLs.

    Use this when you need to find current information, facts, or references.
    No API key required.
    """
    results = search(query, limit=limit)
    return [
        {"title": r["title"], "url": r["url"]}
        for r in results
    ]


@mcp.tool()
def web_extract(urls: list[str]) -> list[dict]:
    """Extract readable text content from web pages.

    Returns text content for each URL (capped at 5000 chars).
    Use after web_search to read the full content of a page.
    """
    results = []
    for url in urls:
        content = extract(url, max_chars=5000)
        results.append({
            "url": url,
            "content": content,
            "content_length": len(content),
        })
    return results


@mcp.tool()
def web_search_and_extract(query: str, limit: int = 3) -> list[dict]:
    """Search the web AND extract full content from results in one call.

    Combines web_search + web_extract for efficiency.
    """
    results = search_and_extract(query, limit=limit)
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", "")[:3000],
        }
        for r in results
    ]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
