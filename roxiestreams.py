import requests
from bs4 import BeautifulSoup
import re
import json
import os

# The main URL
BASE_URL = "https://roxiestreams.live"
SOCCER_URL = f"{BASE_URL}/soccer"

def scrape_streams():
    results = []
    print(f"Connecting to {SOCCER_URL}...")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(SOCCER_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Find all potential match links
        # We look for links that contain 'soccer' or look like subpages
        all_links = soup.find_all('a', href=True)
        match_links = []
        
        for l in all_links:
            href = l['href']
            # Filter for links that likely lead to a player page
            if "/soccer/" in href and href != "/soccer":
                full_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                if full_url not in match_links:
                    match_links.append((l.text.strip(), full_url))

        print(f"Found {len(match_links)} potential matches. Extracting streams...")

        for title, m_url in match_links:
            try:
                m_res = requests.get(m_url, headers=headers, timeout=10)
                # Regex to capture the URL inside showPlayer('clappr', 'URL')
                # It handles both single and double quotes
                links = re.findall(r"showPlayer\s*\(\s*['\"].*?['\"]\s*,\s*['\"](https?://.*?\.(?:m3u8|mp4|m3u))['\"]\s*\)", m_res.text)
                
                if links:
                    results.append({
                        "match_title": title if title else "Untitled Match",
                        "match_url": m_url,
                        "m3u8_links": list(set(links)) # remove duplicates
                    })
                    print(f"  [✔] Found {len(links)} links for: {title}")
            except Exception as e:
                print(f"  [!] Error on {m_url}: {e}")

        # 2. Save to data/roxiestreams.json
        os.makedirs('data', exist_ok=True)
        with open('data/roxiestreams.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        print(f"\nDone! Saved {len(results)} matches to data/roxiestreams.json")

    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    scrape_streams()
