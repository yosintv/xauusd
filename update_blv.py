import json
import re
from curl_cffi import requests

def clean_name(name):
    if not name: return "TBA"
    # Removes common football suffixes for a cleaner display
    return re.sub(r'\b(FC|FK|SC|AFC|CF|CC|U23|U21|U19|W|JK|United|City)\b', '', name, flags=re.IGNORECASE).strip()

def fetch_data():
    url = "https://socolive.club/api/v1/match?t=456"
    
    try:
        # Using impersonate="chrome" to bypass 403 Forbidden errors
        response = requests.get(url, impersonate="chrome")
        response.raise_for_status()
        
        raw_data = response.json()
        matches = raw_data.get("data", [])
        
        output = []
        for match in matches:
            # Skip if it's not a football match (categoryId 1) if you only want football
            # if match.get("categoryId") != 1: continue

            team1 = clean_name(match.get("hostName"))
            team2 = clean_name(match.get("guestName"))
            title = f"{team1} vs {team2}"
            
            # Extract UIDs from the 'anchors' list
            anchors = match.get("anchors", [])
            uids = [str(a.get("uid")) for a in anchors]
            
            # Construct the YoSinTV formatted entry
            # We use uids[0] for link 3, uids[1] for link 5, etc.
            match_entry = {
                "name": title,
                "links": [
                    "https://yosintv2.github.io/ads/foot.html?url=https://ytvlive.pages.dev/akk?m=_______",
                    "https://yosintv-api.pages.dev/api/ads",
                    f"https://yosintv2.github.io/ads/foot.html?url=https://ytvlive.pages.dev/ak?m={uids[0] if len(uids) > 0 else 'offline'}",
                    "https://yosintv-api.pages.dev/api/ads",
                    f"https://yosintv2.github.io/ads/foot.html?url=https://ytvlive.pages.dev/ak?m={uids[1] if len(uids) > 1 else (uids[0] if uids else 'offline')}",
                    f"https://yosintv2.github.io/ads/foot.html?url=https://ytvlive.pages.dev/ak?m={uids[2] if len(uids) > 2 else (uids[0] if uids else 'offline')}"
                ]
            }
            output.append(match_entry)

        with open("blv.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            
        print(f"Update Successful! Processed {len(output)} matches into blv.json.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_data()
