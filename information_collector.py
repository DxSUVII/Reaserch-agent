import os 
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
from helper import get_serpapi_url, get_patent_data_from_serpapi

load_dotenv()

def fetch_patent_data(query,dir_path):
    """
    fetch patent data from serp api and save it to thte specified directory.
    Args:
        query(str): Search query for patenst
        dir_path(str): Direcotry to save the results
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        raise ValueError("SERP_API_KEY variable is not set")

    # Ensure the output directory exists
    os.makedirs(dir_path,exist_ok=True)

    url=(
        f"https://serpapi.com/search.json?engine=google_patents&q={query}&api_key={api_key}"
    )
    response= requests.get(url)
    if response.status_code != 200:
        print(f"ERror fetching data:{response.status_code},{response.text}")
        exit(1)

    if response.status_code == 200:
        data = response.json()
        for idx, patent in enumerate(data.get("organic_results", [])):
            serpapi_url = get_serpapi_url(patent)
            response_data = get_patent_data_from_serpapi(serpapi_url)

            if not response_data:
                print(f"Error fetching data for patent {idx}: No data returned")
                continue
            
            with open(f"{dir_path}/patent_data_{idx}.json", "w") as f:
                json.dump(response_data, f, indent=4)
            patent_citations = response_data.get("patent_citations", {}).get(
                "original", []
            )

            for idx2, citations in enumerate(patent_citations):
                serpapi_url2 = citations.get("serpapi_url", None)
                if serpapi_url2:
                    citations_data = get_patent_data_from_serpapi(serpapi_url2)
                    if citations_data:
                        with open(f"{dir_path}/citations_{idx}_{idx2}.json", "w") as f:
                            json.dump(citations_data, f, indent=4)
                    else:
                        print(
                            f"Error fetching data for citation {idx2}: No data returned,"
                        )
                else:
                    print(f"No serpapi_url found for citations {idx2}.")
    else:
        print(f"Error: {response.status_code},{response.text}")

            

if __name__ == "__main__":
    query = input("Enter your search query for patents:")
    dir_path = "results/patents"
    try:
        fetch_patent_data(query,dir_path)
        print("Patent data fetched and saved successfully.")
    except Exception as e:
        print("Am an error occurred:", e)