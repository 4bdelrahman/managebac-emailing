"""
Gmail Label Management Module
Purpose: Creates and applies Gmail labels to emails
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
from dotenv import load_dotenv
from utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging("apply_label")


def get_or_create_label(service, label_name):
    """
    Get label ID if exists, or create it if it doesn't.
    
    Args:
        service: Authenticated Gmail API service
        label_name: Name of the label to get/create
        
    Returns:
        Label ID string
    """
    try:
        # List all labels
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        # Check if label already exists
        for label in labels:
            if label['name'].lower() == label_name.lower():
                logger.info(f"Label '{label_name}' already exists with ID: {label['id']}")
                return label['id']
        
        # Label doesn't exist, create it
        logger.info(f"Creating new label: {label_name}")
        label_object = {
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
        
        created_label = service.users().labels().create(
            userId='me',
            body=label_object
        ).execute()
        
        logger.info(f"✅ Created label '{label_name}' with ID: {created_label['id']}")
        return created_label['id']
        
    except Exception as e:
        logger.error(f"Error getting/creating label: {e}")
        raise


def apply_label_to_email(service, email_id, label_id):
    """
    Apply a label to a specific email.
    
    Args:
        service: Authenticated Gmail API service
        email_id: Email message ID
        label_id: Label ID to apply
        
    Returns:
        Boolean: True if successful, False otherwise
    """
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'addLabelIds': [label_id]}
        ).execute()
        
        logger.info(f"✅ Applied label to email {email_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error applying label to email {email_id}: {e}")
        return False


def remove_label_from_email(service, email_id, label_id):
    """
    Remove a label from a specific email.
    
    Args:
        service: Authenticated Gmail API service
        email_id: Email message ID
        label_id: Label ID to remove
        
    Returns:
        Boolean: True if successful, False otherwise
    """
    try:
        service.users().messages().modify(
            userId='me',
            id=email_id,
            body={'removeLabelIds': [label_id]}
        ).execute()
        
        logger.info(f"Removed label from email {email_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error removing label from email {email_id}: {e}")
        return False


def list_user_labels(service):
    """
    List all labels for the user (debugging).
    
    Args:
        service: Authenticated Gmail API service
        
    Returns:
        List of label dictionaries
    """
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        logger.info(f"Found {len(labels)} labels")
        for label in labels:
            logger.info(f"  - {label['name']} (ID: {label['id']})")
        
        return labels
        
    except Exception as e:
        logger.error(f"Error listing labels: {e}")
        return []


if __name__ == "__main__":
    from gmail_auth import get_gmail_service
    
    print("Testing Label Management...")
    print("-" * 50)
    
    try:
        service = get_gmail_service()
        label_name = os.getenv('MANAGEBAC_LABEL_NAME', 'ManageBac')
        
        # Test getting/creating label
        label_id = get_or_create_label(service, label_name)
        print(f"\n✅ Label '{label_name}' ID: {label_id}")
        
        # List all labels
        print("\nAll labels:")
        list_user_labels(service)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
