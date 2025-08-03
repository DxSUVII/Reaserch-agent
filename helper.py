import os  # For accessing environment variables
import requests  # For making HTTP requests to APIs
import json  # For handling JSON data
from pprint import pprint  # For pretty-printing data (mainly for debugging)
from dotenv import load_dotenv  # For loading environment variables from a .env file

load_dotenv()  # Load environment variables from .env file into the system

api_key = os.getenv("SERP_API_KEY")  # Get the SerpApi key from environment variables
if not api_key:
    # If the API key is missing, stop the program and show an error
    raise ValueError("SERP_API_KEY variable is not set")


def get_serpapi_url(data):
    """
    Constructs the SerpApi URL for the given data.
    Args:
        data (dict): The data containing the SerpApi link.
    Returns:
        str: The complete SerpApi URL with the API key.
    """
    # Check if the required key is present in the input dictionary
    if "serpapi_link" not in data:
        # If not, raise an error to prevent further issues
        raise ValueError("The provided data does not contain the serpapi_link.")
    # Extract the URL from the input data
    serpapi_url = data["serpapi_link"]

    # If the API key is not already in the URL, add it
    if "api_key=" not in serpapi_url:
        # Decide whether to use '&' or '?' based on existing query parameters
        separator = "&" if "?" in serpapi_url else "?"
        # Append the API key to the URL using the correct separator
        serpapi_url = f"{serpapi_url}{separator}api_key={api_key}"

    # Return the final URL with the API key included
    return serpapi_url


def get_patent_data_from_serpapi(serpapi_url):
    """
    Fetches patent data from the SerpApi URL.

    Args:
        serpapi_url (str): The SerpApi URL to fetch data from.
    Returns:
        dict: The patent data fetched from the SerpApi.
    Raised:
        HTTPError: If the request returns an error status code.
    """
    # Prepare the parameters for the GET request (API key included for safety)
    params = {"api_key": api_key}
    # Make the GET request to the SerpApi URL
    response = requests.get(serpapi_url, params=params)

    # If the request was successful (HTTP 200 OK)
    if response.status_code == 200:
        # Parse and return the JSON data from the response
        return response.json()
    else:
        # If there was an error, raise an exception to notify the caller
        response.raise_for_status()