from mcp.server.fastmcp import FastMCP
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


mcp = FastMCP('check_internet_connection')

@mcp.tool(
    name="check_internet_connection",
    description="Tool to check if there is an internet connection available by pinging google.com."
)
def check_internet_connection() -> str:
    """
    Tool to check if we have an internet connection by pinging google.com.
    
    Inputs:
        - None
    
    Returns:
        - If successful, it returns a string with its respective response code
    """
    
    try:
        response = requests.get('https://www.google.com', timeout=5)
        logger.info(f"Response:\n\n{response}")
        return f"We have an internet connection! (Status Code: {response.status_code})"

    except Exception as e:
        return f"No internet connection! Response: {e})"


if __name__ ==  "__main__":
    mcp.run(transport='stdio')