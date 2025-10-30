from mcp.server.fastmcp import FastMCP
import requests
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


mcp = FastMCP('wikipedia-search')

@mcp.tool()
def search_wikipedia(subject: str) -> str:
    """
    Tool to query the wikipedia API to search for articles (subject) related to a given query. 
    The subject query must be provided as input and must be short and consise. It should not be a full sentence.
    The tool should return the extract of the article(s) found in the search as a parsable JSON object.
    
    You will need to tidy the information before passing it to the user.
    """
    
    url = 'https://en.wikipedia.org/w/api.php'

    headers = {
        'User-Agent': 'MCPPythonBot-personal-use'
    }
    
    params = {
            'action': 'query',
            'format': 'json',
            'titles': subject,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }

    logging.info(f"Parameters: {json.dumps(params)}")
    logging.info(f"URL: {url}")
    logging.info(f"Headers: {json.dumps(headers)}")
    logging.info(f"Searching Wikipedia for subject: {subject}")
    
    response = requests.get(
        url, 
        params = params, 
        headers = headers
        )

    return response.text
 
def main():
    mcp.run(transport='stdio')

if __name__ ==  "__main__":
    main()