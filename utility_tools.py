from langchain_core.tools import tool
from models import pipeline
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages.tool import ToolMessage
import tempfile

@tool
def make_images_api(image_text_prompt: str) -> str:
    """
    Generate an image based on the text prompt using the pipeline and save it to a temporary path and return the save path of image.
    
    Args:
        image_text_prompt (str): The text prompt for the image generation.
    
    Returns:
        str: Path to the saved image.
    """
    image = pipeline(prompt=image_text_prompt).images[0]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_path = temp_file.name
        image.save(temp_path, format="PNG")
    
    return temp_path

@tool
def search_in_web(users_query: str):
    """
    Perform a web search using DuckDuckGo and return the search results.

    This function uses the DuckDuckGoSearchResults tool to execute a web search
    based on the provided query. It prints the search results and returns them 
    for further processing.

    Args:
        users_query (str): The search query to be performed on the web.
    
    Returns:
        The search results from DuckDuckGo, typically a list or dict containing 
        search result information.

    Example:
        >>> search_results = search_in_web("Python programming")
        # This will print the search results and return them
    """
    result = DuckDuckGoSearchResults()
    res = result.invoke(users_query)
    return res


tool_mapping = {
    "make_images_api" : make_images_api,
    "search_in_web" : search_in_web
}


