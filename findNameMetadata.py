import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# Replace with your own Google API key and Custom Search Engine ID
API_KEY = 'your_google_api_key'
SEARCH_ENGINE_ID = 'your_custom_search_engine_id'

def google_search(query, api_key, cse_id, **kwargs):
    """Performs a Google search using the Custom Search API."""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res['items']

def fetch_metadata(url):
    """Fetches metadata from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata tags
        metadata = {}
        for tag in soup.find_all('meta'):
            if 'name' in tag.attrs and 'content' in tag.attrs:
                metadata[tag.attrs['name']] = tag.attrs['content']
            elif 'property' in tag.attrs and 'content' in tag.attrs:
                metadata[tag.attrs['property']] = tag.attrs['content']

        return metadata
    except Exception as e:
        print(f"Error fetching metadata from {url}: {e}")
        return None

def search_and_scrape(query):
    """Searches Google and scrapes metadata for given query."""
    print(f"Searching for '{query}' on the web...")
    
    # Step 1: Perform Google Search
    results = google_search(query, API_KEY, SEARCH_ENGINE_ID, num=5)

    # Step 2: Loop through search results and scrape metadata
    for result in results:
        url = result['link']
        print(f"\nFetching metadata for: {url}")
        metadata = fetch_metadata(url)
        if metadata:
            print(f"Metadata for {url}:")
            for key, value in metadata.items():
                print(f"{key}: {value}")
        else:
            print("No metadata found.")

# Replace 'Your Name' with your actual name
search_and_scrape('Your Name')
