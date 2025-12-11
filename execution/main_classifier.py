"""
Main Email Classifier Orchestrator
Purpose: Orchestrates the complete email classification workflow
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from gmail_auth import get_gmail_service
from fetch_emails import fetch_unprocessed_emails, get_email_content
from classify_email import classify_email
from apply_label import get_or_create_label, apply_label_to_email
from utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging("main_classifier")


def main():
    """
    Main workflow orchestrator.
    
    Process:
    1. Authenticate with Gmail
    2. Get or create ManageBac label
    3. Fetch unprocessed emails
    4. Classify each email with AI
    5. Apply label to ManageBac-related emails
    6. Log results
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting ManageBac Email Classifier")
    logger.info(f"Timestamp: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Step 1: Authenticate with Gmail
        logger.info("Step 1: Authenticating with Gmail...")
        service = get_gmail_service()
        
        # Step 2: Get or create ManageBac label
        label_name = os.getenv('MANAGEBAC_LABEL_NAME', 'ManageBac')
        logger.info(f"Step 2: Getting/creating label '{label_name}'...")
        label_id = get_or_create_label(service, label_name)
        
        # Step 3: Fetch unprocessed emails
        max_emails = int(os.getenv('MAX_EMAILS_PER_RUN', 50))
        logger.info(f"Step 3: Fetching up to {max_emails} unprocessed emails...")
        emails = fetch_unprocessed_emails(service, max_results=max_emails)
        
        if not emails:
            logger.info("✅ No unprocessed emails found. All done!")
            return
        
        logger.info(f"Found {len(emails)} emails to process")
        
        # Step 4 & 5: Process each email
        stats = {
            'total': len(emails),
            'managebac': 0,
            'not_managebac': 0,
            'errors': 0
        }
        
        for i, email in enumerate(emails, 1):
            try:
                logger.info(f"\n{'='*60}")
                logger.info(f"Processing email {i}/{len(emails)}")
                logger.info(f"{'='*60}")
                
                # Get email content
                content = get_email_content(service, email['id'])
                if not content:
                    logger.error(f"Failed to get content for email {email['id']}")
                    stats['errors'] += 1
                    continue
                
                logger.info(f"From: {content['sender']}")
                logger.info(f"Subject: {content['subject']}")
                
                # Classify with AI
                is_managebac = classify_email(
                    content['subject'],
                    content['sender'],
                    content['body']
                )
                
                # Apply label if ManageBac-related
                if is_managebac:
                    success = apply_label_to_email(service, email['id'], label_id)
                    if success:
                        stats['managebac'] += 1
                        logger.info(f"✅ LABELED as ManageBac")
                    else:
                        stats['errors'] += 1
                        logger.error(f"Failed to apply label")
                else:
                    stats['not_managebac'] += 1
                    logger.info(f"⏭️  SKIPPED (not ManageBac-related)")
                
            except Exception as e:
                logger.error(f"Error processing email {email['id']}: {e}")
                stats['errors'] += 1
        
        # Step 6: Log results
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("\n" + "=" * 60)
        logger.info("WORKFLOW COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total emails processed: {stats['total']}")
        logger.info(f"  ✅ Labeled as ManageBac: {stats['managebac']}")
        logger.info(f"  ⏭️  Not ManageBac: {stats['not_managebac']}")
        logger.info(f"  ❌ Errors: {stats['errors']}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Timestamp: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # Summary
        if stats['managebac'] > 0:
            logger.info(f"\n🎉 Successfully labeled {stats['managebac']} ManageBac emails!")
        else:
            logger.info("\n📭 No ManageBac emails found in this batch.")
        
    except Exception as e:
        logger.error(f"\n❌ CRITICAL ERROR: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Workflow interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Workflow failed: {e}")
        exit(1)
