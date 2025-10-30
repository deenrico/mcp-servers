import asyncio
from crawl4ai import *
from mcp.server.fastmcp import FastMCP
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

mcp = FastMCP("web-search")

@mcp.tool(name = "Web Search")
async def brave_web_search(
    search_term: str
    ) -> str:
    """Tool to search the brave web search and scrap it's results. 
    Resulting links can be used to further search the web using
    the deep_search tool.

    Args:
        search_term (str): A search query to send to the Brave search engine.

    Returns:
        str: The raw, scraped webpage as markdown, including further links to deep search.
    """
    
    search_term_parsed = search_term.replace(" ", "+")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"https://search.brave.com/search?q={search_term_parsed}",
        )
        
        logger.info(f'### Scraped search engine results (raw):\n\n{result.markdown}')
        
        return result.markdown

@mcp.tool(name = "Deep Search")
async def deep_search(link: str) -> str:
    """Tool to further search links found in the initial search engine search.

    Args:
        link (str): Link from the initial search engine results.

    Returns:
        str: The accessed webpage.
    """
    
    # try:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=link,
        )
        
        logger.info(f'### Scraped deep webpage:\n\n{result.markdown}')
        
        return result.markdown
        
    # except Exception as e:
    #     return f"Scrap request failed with error {e}"

if __name__ == "__main__":
    # TESTING
    # asyncio.run(brave_web_search("Daniel Noboa"))
    mcp.run(transport='stdio')
