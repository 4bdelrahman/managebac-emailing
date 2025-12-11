"""
Email Classification Module
Purpose: Classifies emails using Groq AI to identify ManageBac-related emails
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
from groq import Groq
from dotenv import load_dotenv
from utils import setup_logging, retry_with_exponential_backoff

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging("classify_email")

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def classify_email(subject, sender, body):
    """
    Classify if an email is ManageBac-related using Groq AI.
    
    Args:
        subject: Email subject line
        sender: Email sender address
        body: Email body content
        
    Returns:
        Boolean: True if ManageBac-related, False otherwise
    """
    try:
        # Quick check: If sender is from @managebac.com, it's definitely ManageBac
        if '@managebac.com' in sender.lower():
            logger.info(f"Auto-classified as ManageBac (sender: {sender})")
            return True
        
        # Otherwise, use AI classification
        prompt = build_classification_prompt(subject, sender, body)
        
        # Use retry logic for API calls
        def make_api_call():
            response = groq_client.chat.completions.create(
                model=os.getenv('GROQ_MODEL', 'openai/gpt-oss-120b'),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an email classifier. Respond with ONLY 'YES' or 'NO'."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent classification
                max_tokens=10
            )
            return response
        
        response = retry_with_exponential_backoff(make_api_call, max_attempts=3)
        
        # Parse response
        result = parse_ai_response(response)
        
        logger.info(f"Classification result for '{subject[:50]}...': {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error classifying email: {e}")
        # Fallback to keyword-based classification
        return fallback_classification(subject, sender, body)


def build_classification_prompt(subject, sender, body):
    """
    Build the classification prompt for the AI.
    
    Args:
        subject: Email subject
        sender: Email sender
        body: Email body (first 500 chars)
        
    Returns:
        Formatted prompt string
    """
    # Truncate body to first 500 characters
    body_preview = body[:500] if body else "No body content"
    
    prompt = f"""You are classifying emails for a student using ManageBac (school management platform).

IMPORTANT RULES:
1. If the sender contains "@managebac.com" → ALWAYS answer YES
2. If the email mentions IB subjects (DP, MYP, CP), assignments, or school activities → answer YES
3. If it's about CAS, TOK, Extended Essay, or IB coursework → answer YES
4. If it's promotional, marketing, or unrelated to school → answer NO

ManageBac-related indicators:
- Sender: @managebac.com, school domains, teacher emails
- Keywords: ManageBac, IB DP/MYP, assignment, submission, grade, CAS, TOK, coursework, due date, teacher comment
- Content: School announcements, academic tasks, student activities

Email to classify:
From: {sender}
Subject: {subject}
Body: {body_preview}

Question: Is this email related to ManageBac or school activities?
Answer with ONLY "YES" or "NO"."""

    return prompt


def parse_ai_response(response):
    """
    Parse the AI response to extract classification result.
    
    Args:
        response: Groq API response object
        
    Returns:
        Boolean: True if YES, False if NO
    """
    try:
        content = response.choices[0].message.content.strip().upper()
        
        # Look for YES or NO in the response
        if 'YES' in content:
            return True
        elif 'NO' in content:
            return False
        else:
            logger.warning(f"Unexpected AI response: {content}")
            return False
            
    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        return False


def fallback_classification(subject, sender, body):
    """
    Fallback keyword-based classification if AI fails.
    
    Args:
        subject: Email subject
        sender: Email sender
        body: Email body
        
    Returns:
        Boolean: True if likely ManageBac-related
    """
    logger.info("Using fallback keyword-based classification")
    
    # Combine all text
    all_text = f"{subject} {sender} {body}".lower()
    
    # ManageBac-related keywords
    keywords = [
        'managebac',
        '@managebac.com',
        'cas reflection',
        'tok',
        'ib diploma',
        'ib dp',
        'ib myp',
        'assignment submitted',
        'grade posted',
        'due date',
        'coursework',
        'academic',
        'teacher comment'
    ]
    
    # Check if any keyword is present
    for keyword in keywords:
        if keyword in all_text:
            logger.info(f"Matched keyword: {keyword}")
            return True
    
    return False


if __name__ == "__main__":
    print("Testing Email Classification...")
    print("-" * 50)
    
    # Test cases
    test_emails = [
        {
            "subject": "New assignment posted in Math HL",
            "sender": "noreply@managebac.com",
            "body": "A new assignment has been posted in your Math HL course. Due date: Dec 15"
        },
        {
            "subject": "Amazon Order Confirmation",
            "sender": "auto-confirm@amazon.com",
            "body": "Your order #123456 has been shipped"
        },
        {
            "subject": "CAS Reflection Due Tomorrow",
            "sender": "teacher@school.com",
            "body": "Don't forget to submit your CAS reflection on ManageBac"
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        result = classify_email(
            email['subject'],
            email['sender'],
            email['body']
        )
        print(f"\nTest {i}: {email['subject']}")
        print(f"Result: {'✅ ManageBac' if result else '❌ Not ManageBac'}")
