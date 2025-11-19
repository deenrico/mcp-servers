import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
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
    """Tool to search the brave web search and scrape it's results. 
    This can be used whenever there is not sufficient information on the topic or no
    other available tool that could help.
    Resulting links can be used to further search the web using
    the deep_search tool.

    Args:
        search_term (str): A search query to send to the Brave search engine.

    Returns:
        dict: A dictionary of the cleaned, scraped webpage as markdown, 
              including external links and media sources to deep search if necessary.
    """
    
    search_term_parsed: str = search_term.replace(" ", "+")
    
    crawl_config = CrawlerRunConfig(
        # word_count_threshold=100,
        excluded_tags=['form', 'header'],
        exclude_external_links=False,
        process_iframes=True,
        remove_overlay_elements=True,
        # cache_mode=CacheMode.ENABLED
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            
            # TODO: Find way to circumvent new bot detection on brave SE
            url = f"https://search.brave.com/search?q={search_term_parsed}",
            # url=f"https://duckduckgo.com/?q={search_term_parsed}",
            config=crawl_config
        )
        
        if result.success:
        
            crawl_dict = {
                'markdown':result.markdown.fit_markdown, 
                'links': result.links,
                'media': result.media
                }
            
            logger.info('SUCCESS')
            logger.info(f'{crawl_dict}')
            
            return str(crawl_dict)
        
        else:
            
            logger.info('ERROR')
            logger.info(f'{result.error_message}')
            
            return f'Web scraping failed with error {result.error_message}'


@mcp.tool(name = "Deep Search")
async def deep_search(link: str) -> str:
    """Tool to further search links found in the initial search engine search.
    This is useful whenever the initial search did not provide enough information.

    Args:
        link (str): Link from the initial search engine results.

    Returns:
        str: The accessed webpage.
    """
    
    crawl_config = CrawlerRunConfig(
        excluded_tags=['form', 'header'],
        exclude_external_links=False,
        process_iframes=True,
        remove_overlay_elements=True,
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=link,
            # config=crawl_config
        )
        
        if result.success:
        
            crawl_dict = {
                'markdown':result.markdown.fit_markdown, 
                'links': result.links,
                'media': result.media
                }
            
            logger.info('SUCCESS')
            logger.info(f'{crawl_dict}')
            
            return str(crawl_dict)
        
        else:
            
            logger.info('ERROR')
            logger.info(f'{result.error_message}')
            
            return f'Web scraping failed with error {result.error_message}'


if __name__ == "__main__":
    # TODO: move testing to tests
    # asyncio.run(brave_web_search("Daniel Noboa"))
    mcp.run(transport='stdio')
