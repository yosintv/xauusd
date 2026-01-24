import requests
from bs4 import BeautifulSoup
import re
import json
import os

URL = "https://roxiestreams.live/soccer"

def scrape_streams():
    results = []
    try:
        # Fetch the main page
        response = requests.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the links in the table (based on common sports site layouts)
        match_rows = soup.find_all('a', href=True)
        
        for row in match_rows:
            match_url = row['href']
            if not match_url.startswith('http'):
                match_url = f"https://roxiestreams.live{match_url}"
            
            # Skip non-match links
            if "/soccer/" not in match_url:
                continue
                
            try:
                # Visit the specific match page
                match_page = requests.get(match_url, timeout=10)
                # Extract links from the showPlayer function
                m3u8_links = re.findall(r"showPlayer\('.*?',\s*'(.*?)'\)", match_page.text)
                
                if m3u8_links:
                    results.append({
                        "match_title": row.text.strip(),
                        "match_url": match_url,
                        "m3u8_links": m3u8_links
                    })
            except Exception as e:
                print(f"Error scraping match page {match_url}: {e}")

        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Save to JSON
        with open('data/roxiestreams.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("Successfully updated data/roxiestreams.json")

    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    scrape_streams()
