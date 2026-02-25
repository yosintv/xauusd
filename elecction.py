import requests
import json
import os

def fetch_and_convert():
    # The source is a .txt file containing JSON data
    source_url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2082.txt"
    output_filename = "2082.json"
    
    # Headers to mimic a real browser (Prevents the "Line 1 Column 1" error)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        print(f"Fetching data from {source_url}...")
        response = requests.get(source_url, headers=headers, timeout=30)
        
        # Check if the site blocked us (403) or page not found (404)
        response.raise_for_status()
        
        # Clean the text (sometimes .txt files have hidden BOM or whitespace)
        raw_text = response.text.strip()
        
        if not raw_text:
            print("Error: The .txt file is empty.")
            return

        # Parse the text as JSON
        json_data = json.loads(raw_text)
        
        # Save it as a properly formatted .json file
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully converted .txt to {output_filename}")
        
    except requests.exceptions.HTTPError as e:
        print(f"Server Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Data Error: The .txt file does not contain valid JSON.")
        print(f"Content received: {response.text[:100]}...") # Show first 100 chars
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    fetch_and_convert()
