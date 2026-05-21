"""MCP server for DuckDuckGo web search."""

from mcp.server.fastmcp import FastMCP
from websearch import search, extract, search_and_extract

mcp = FastMCP("Web Search")


@mcp.tool()
def web_search(query: str, limit: int = 5) -> list[dict]:
    """Search the web via DuckDuckGo. Returns titles, URLs, and descriptions.

    Use this when you need to find current information, facts, or references.
    No API key required.
    """
    results = search(query, limit=limit)
    return [
        {"title": r.title, "url": r.url, "description": r.description}
        for r in results
    ]


@mcp.tool()
def web_extract(urls: list[str]) -> list[dict]:
    """Extract readable text content from web pages.

    Returns markdown-formatted content for each URL.
    Use after web_search to read the full content of a page.
    """
    results = extract(urls)
    return [
        {
            "url": r.url,
            "title": r.title,
            "content": r.content[:5000],  # cap for LLM context
            "content_length": len(r.content),
        }
        for r in results
    ]


@mcp.tool()
def web_search_and_extract(query: str, limit: int = 3) -> list[dict]:
    """Search the web AND extract full content from results in one call.

    Combines web_search + web_extract for efficiency.
    """
    results = search_and_extract(query, limit=limit)
    return [
        {
            "title": r.title,
            "url": r.url,
            "description": r.description,
            "content": r.content[:3000] if r.content else "",
        }
        for r in results
    ]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
