import requests
import json

def fetch_and_save():
    source_url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    filename = "2082.json"
    
    # Adding a User-Agent makes the server think a browser is requesting the data
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"Fetching data from {source_url}...")
        response = requests.get(source_url, headers=headers, timeout=30)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Check if content is empty
        if not response.text.strip():
            print("Error: The server returned an empty response.")
            return

        # Try to parse JSON
        data = response.json()
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully updated {filename}")
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except json.JSONDecodeError:
        print("Error: The content received is not valid JSON. It might be an HTML error page.")
        print("Raw Content Preview:", response.text[:200]) # Shows first 200 chars for debugging
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_and_save()
