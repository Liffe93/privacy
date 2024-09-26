import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse, urljoin

# Function to build a regex for the user's phone number (handles multiple formats)
def build_phone_regex(phone_number):
    # Escape the phone number for regex (in case it contains special characters)
    escaped_phone = re.escape(phone_number)
    # Handle common formats like with spaces, dashes, or parentheses
    phone_regex = f"\\b{escaped_phone[:3]}[-.\\s]?{escaped_phone[3:6]}[-.\\s]?{escaped_phone[6:]}\\b"
    return phone_regex

# Function to extract and search for user's PII in metadata
def extract_metadata(url, user_name_regex, user_phone_regex):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all metadata
        metadata = soup.find_all('meta')
        pii_found = []

        # Search metadata for the user's name and phone number
        for meta in metadata:
            content = meta.get('content', '')
            if content:
                # Search for the user's name
                if re.search(user_name_regex, content, re.IGNORECASE):
                    pii_found.append(f"Name match: {content}")
                
                # Search for the user's phone number
                if re.search(user_phone_regex, content):
                    pii_found.append(f"Phone match: {content}")
        
        return pii_found

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

# Function to crawl all pages within a domain and search for user's PII
def crawl_domain(start_url, user_name_regex, user_phone_regex, max_depth=3):
    visited = set()  # To keep track of visited URLs
    to_visit = [start_url]  # Queue of URLs to visit

    base_domain = urlparse(start_url).netloc

    # Open the output file to save URLs with detected PII in metadata
    with open('pii_matches.txt', 'a') as f:  # Append mode
        while to_visit and max_depth > 0:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue

            print(f"Visiting: {current_url}")
            visited.add(current_url)

            pii_data = extract_metadata(current_url, user_name_regex, user_phone_regex)
            if pii_data:
                print(f"PII found on {current_url}: {pii_data}")
                # Write the URL and matched PII details to the file
                f.write(f"URL: {current_url}\n")
                for pii in pii_data:
                    f.write(f"  - {pii}\n")
                f.write("\n")
            else:
                print(f"No PII found on {current_url}")

            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all anchor tags and follow links
                for a_tag in soup.find_all('a', href=True):
                    next_url = urljoin(current_url, a_tag['href'])
                    next_url_parsed = urlparse(next_url)

                    # Ensure we stay within the same domain
                    if next_url_parsed.netloc == base_domain and next_url not in visited:
                        to_visit.append(next_url)

            except requests.RequestException as e:
                print(f"Error crawling {current_url}: {e}")

            # Wait to avoid hammering the server
            time.sleep(2)
            max_depth -= 1

# User input for PII search
user_name = input("Enter your full name to search: ")
user_phone = input("Enter your phone number to search: ")

# Build regex patterns for name and phone number
user_name_regex = re.escape(user_name)  # Escape the user's name for regex
user_phone_regex = build_phone_regex(user_phone)

# Starting URL (base domain)
start_url = 'https://example.com'  # Replace with the domain you want to crawl

# Start crawling the entire domain and searching for the user's PII
crawl_domain(start_url, user_name_regex, user_phone_regex)
