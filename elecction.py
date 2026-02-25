import requests
import json

def fetch_and_convert():
    source_url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    output_filename = "2082.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    
    try:
        print(f"Fetching data from {source_url}...")
        response = requests.get(source_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Use 'utf-8-sig' to automatically strip the ï»¿ (BOM) characters
        response.encoding = 'utf-8-sig'
        raw_text = response.text.strip()
        
        # Manual fallback: if the BOM is still there, strip it manually
        if raw_text.startswith('\ufeff'):
            raw_text = raw_text.lstrip('\ufeff')
        
        # Parse the cleaned text as JSON
        json_data = json.loads(raw_text)
        
        # Save as a clean .json file
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully converted and saved to {output_filename}")
        
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        # Last resort: print the first few characters to see what's left
        print(f"Start of text: {raw_text[:50]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_convert()
