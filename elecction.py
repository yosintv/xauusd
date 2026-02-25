import requests
import json

def fetch_and_save():
    # The source URL (raw text/json from Election Commission)
    source_url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    filename = "2082.json"
    
    try:
        print(f"Fetching data from {source_url}...")
        response = requests.get(source_url, timeout=15)
        response.raise_for_status()
        
        # Parse content as JSON to ensure it's valid
        data = response.json()
        
        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully updated {filename}")
        
    except Exception as e:
        print(f"Error updating data: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
