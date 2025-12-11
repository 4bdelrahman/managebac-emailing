"""
Gmail Authentication Module
Purpose: Handles Gmail OAuth authentication and token management
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

def get_gmail_service():
    """
    Authenticates and returns Gmail API service instance.
    
    Returns:
        Gmail API service object
        
    Raises:
        Exception: If authentication fails
    """
    creds = None
    token_file = 'token.json'
    credentials_file = os.getenv('GMAIL_CREDENTIALS_FILE', 'client_secret.json')
    
    # Check if token.json exists and load credentials
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")
            creds = None
    
    # If credentials are invalid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing access token...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"Credentials file '{credentials_file}' not found. "
                    "Please ensure client_secret.json is in the root directory."
                )
            
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"✅ Credentials saved to {token_file}")
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        print("✅ Gmail authentication successful")
        return service
    except Exception as e:
        raise Exception(f"Failed to build Gmail service: {e}")


def test_authentication():
    """Test Gmail authentication and print user email."""
    try:
        service = get_gmail_service()
        profile = service.users().getProfile(userId='me').execute()
        print(f"\n✅ Authenticated as: {profile['emailAddress']}")
        print(f"Total messages: {profile.get('messagesTotal', 'Unknown')}")
        return True
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing Gmail Authentication...")
    print("-" * 50)
    test_authentication()
