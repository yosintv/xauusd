import requests
import json
import sys

def fetch_and_convert():
    # Target URL
    source_url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    output_filename = "2082.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://result.election.gov.np/"
    }
    
    try:
        print(f"Attempting to fetch data from: {source_url}")
        response = requests.get(source_url, headers=headers, timeout=30)
        
        # Check if the website blocked us (403) or is down (500)
        response.raise_for_status()
        
        # Handle the BOM (ï»¿) characters
        response.encoding = 'utf-8-sig'
        raw_text = response.text.strip()
        
        # Remove manual BOM if still present
        if raw_text.startswith('\ufeff'):
            raw_text = raw_text.lstrip('\ufeff')
        
        # Parse the JSON to ensure it's valid
        json_data = json.loads(raw_text)
        
        # Save the file
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Success! Generated {output_filename}")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code} - The website might be blocking GitHub.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: The data received wasn't valid JSON. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_convert()
