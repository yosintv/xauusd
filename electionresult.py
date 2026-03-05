import requests
import json
import os

def fetch_and_clean(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Handle UTF-8 Byte Order Mark (BOM)
        response.encoding = 'utf-8-sig'
        raw_text = response.text.strip()
        
        # Manual fallback for cleaning
        if raw_text.startswith('\ufeff'):
            raw_text = raw_text.lstrip('\ufeff')
        
        # Parse and Save
        json_data = json.loads(raw_text)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully saved to {filename}")
        return True
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False

if __name__ == "__main__":
    # Source 1: The SecureJson Handler
    url_hor = "https://result.election.gov.np/Handlers/SecureJson.ashx?file=JSONFiles/Election2082/Common/HOR-T5Leader.json"
    fetch_and_clean(url_hor, "HOR-T5Leader.json")

    # Source 2: The Central Result TXT
    url_central = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    fetch_and_clean(url_central, "2082.json")
