import requests
from bs4 import BeautifulSoup
import re
import time

URL = "https://roxiestreams.live/soccer"

def get_stream_links():
    try:
        # 1. Fetch the main page
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. Find all match links (based on your screenshot)
        # We look for 'a' tags that likely lead to the player pages
        match_links = soup.find_all('a', href=True)
        
        streams_found = []

        for link in match_links:
            match_url = link['href']
            # Ensure it's a full URL
            if not match_url.startswith('http'):
                match_url = f"https://roxiestreams.live{match_url}"
            
            try:
                # 3. Visit each match page to find the <button> tags
                match_page = requests.get(match_url, timeout=5)
                # Regex to find .m3u8 links inside showPlayer('...', 'LINK')
                m3u8_links = re.findall(r"showPlayer\('.*?',\s*'(.*?)'\)", match_page.text)
                
                if m3u8_links:
                    match_name = link.text.strip()
                    streams_found.append({
                        "match": match_name,
                        "links": m3u8_links
                    })
            except Exception:
                continue

        # 4. Display results
        print(f"\n--- Updated at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        for item in streams_found:
            print(f"Match: {item['match']}")
            for idx, stream in enumerate(item['links'], 1):
                print(f"  Stream {idx}: {stream}")
                
    except Exception as e:
        print(f"Error fetching data: {e}")

# Run every 1 hour (3600 seconds)
if __name__ == "__main__":
    while True:
        get_stream_links()
        print("\nWaiting 1 hour for next update...")
        time.sleep(3600)
