# Execution Scripts

This folder contains deterministic Python scripts that perform actual work.

## Key Principles

1. **Deterministic** - Same inputs = same outputs, every time
2. **Well-commented** - Explain what each section does
3. **Error handling** - Handle exceptions gracefully
4. **Testable** - Can be run independently for testing
5. **Environment-aware** - Use `.env` for credentials and configuration

## Script Template

```python
"""
Script Name: example_script.py
Purpose: Brief description of what this script does
Author: AI Agent
Last Updated: YYYY-MM-DD
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """
    Main function that executes the script logic.
    """
    try:
        # Your code here
        print("Script executed successfully")
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Use Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
```

### 2. Handle Errors Gracefully
```python
try:
    result = api_call()
except requests.Timeout:
    print("Request timed out, retrying...")
    result = api_call(timeout=60)
except Exception as e:
    print(f"Unexpected error: {e}")
    return None
```

### 3. Use Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('.tmp/script.log'),
        logging.StreamHandler()
    ]
)

logging.info("Starting process...")
```

### 4. Make Scripts Modular
```python
def fetch_data(url):
    """Fetch data from URL"""
    # Implementation

def process_data(data):
    """Process the fetched data"""
    # Implementation

def save_results(results):
    """Save results to destination"""
    # Implementation

def main():
    data = fetch_data(url)
    processed = process_data(data)
    save_results(processed)
```

### 5. Add Retry Logic
```python
import time

def retry(func, max_attempts=3, delay=2):
    """Retry a function up to max_attempts times"""
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                raise e
```

## Common Patterns

### Google Sheets Integration
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('sheets', 'v4', credentials=creds)
```

### Web Scraping
```python
import requests
from bs4 import BeautifulSoup

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')
```

### File Operations
```python
import json

# Write JSON
with open('.tmp/data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Read JSON
with open('.tmp/data.json', 'r') as f:
    data = json.load(f)
```

## Testing Scripts

Always test scripts independently before using them in directives:

```bash
python execution/your_script.py
```

Check logs in `.tmp/` for debugging information.
