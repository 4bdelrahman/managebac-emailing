"""
Email Fetching Module
Purpose: Fetches unprocessed emails from Gmail inbox
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
import base64
from email.mime.text import MIMEText
from dotenv import load_dotenv
from utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging("fetch_emails")


def fetch_unprocessed_emails(service, max_results=50):
    """
    Fetch emails that haven't been processed yet (don't have ManageBac label).
    
    Args:
        service: Authenticated Gmail API service
        max_results: Maximum number of emails to fetch
        
    Returns:
        List of email message IDs and thread IDs
    """
    try:
        label_name = os.getenv('MANAGEBAC_LABEL_NAME', 'ManageBac')
        
        # Query: emails in inbox, not labeled as ManageBac, from last day
        query = f"in:inbox -label:{label_name} newer_than:1d"
        
        logger.info(f"Fetching emails with query: {query}")
        
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        logger.info(f"Found {len(messages)} unprocessed emails")
        
        return messages
        
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return []


def get_email_content(service, email_id):
    """
    Extract email content including subject, sender, and body.
    
    Args:
        service: Authenticated Gmail API service
        email_id: Email message ID
        
    Returns:
        Dictionary with email details (subject, sender, body, snippet)
    """
    try:
        message = service.users().messages().get(
            userId='me',
            id=email_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        
        # Extract subject and sender
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
        
        # Extract email body
        body = parse_email_body(message['payload'])
        
        # Get snippet (short preview)
        snippet = message.get('snippet', '')
        
        return {
            'id': email_id,
            'subject': subject,
            'sender': sender,
            'body': body,
            'snippet': snippet
        }
        
    except Exception as e:
        logger.error(f"Error getting email content for {email_id}: {e}")
        return None


def parse_email_body(payload):
    """
    Parse email body from payload (handles plain text and HTML).
    
    Args:
        payload: Email message payload
        
    Returns:
        Email body text
    """
    body = ""
    
    try:
        # Check if payload has parts (multipart email)
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            # Single part email
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body[:1000]  # Limit to first 1000 characters
        
    except Exception as e:
        logger.error(f"Error parsing email body: {e}")
        return ""


if __name__ == "__main__":
    from gmail_auth import get_gmail_service
    
    print("Testing Email Fetching...")
    print("-" * 50)
    
    try:
        service = get_gmail_service()
        emails = fetch_unprocessed_emails(service, max_results=5)
        
        if emails:
            print(f"\n✅ Found {len(emails)} emails")
            for email in emails[:3]:  # Show first 3
                content = get_email_content(service, email['id'])
                if content:
                    print(f"\nFrom: {content['sender']}")
                    print(f"Subject: {content['subject']}")
                    print(f"Snippet: {content['snippet'][:100]}...")
        else:
            print("✅ No unprocessed emails found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
