"""
Utility functions for the ManageBac Classifier Email System
Purpose: Common helper functions used across execution scripts
Author: AI Agent
Last Updated: 2025-12-11
"""

import os
import logging
from dotenv import load_dotenv
from typing import Any, Optional
import time

# Load environment variables
load_dotenv()


def setup_logging(log_name: str = "app", log_dir: str = ".tmp") -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_name: Name of the logger
        log_dir: Directory to store log files
        
    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # File handler
    log_file = os.path.join(log_dir, f"{log_name}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_env_var(key: str, required: bool = True) -> Optional[str]:
    """
    Get environment variable with optional requirement check.
    
    Args:
        key: Environment variable key
        required: Whether this variable is required
        
    Returns:
        Value of the environment variable or None
        
    Raises:
        ValueError: If required variable is not found
    """
    value = os.getenv(key)
    
    if required and not value:
        raise ValueError(f"Required environment variable '{key}' not found in .env")
    
    return value


def retry_with_exponential_backoff(
    func,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        
    Returns:
        Result of the function call
        
    Raises:
        Last exception if all attempts fail
    """
    logger = setup_logging("retry")
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"All {max_attempts} attempts failed. Last error: {e}")
                raise
            
            delay = min(initial_delay * (exponential_base ** attempt), max_delay)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay)


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Path to the directory
    """
    os.makedirs(directory, exist_ok=True)


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary values.
    
    Args:
        data: Dictionary to get value from
        *keys: Nested keys to traverse
        default: Default value if key not found
        
    Returns:
        Value at the nested key or default
        
    Example:
        safe_get({'a': {'b': {'c': 1}}}, 'a', 'b', 'c')  # Returns 1
        safe_get({'a': {'b': {}}}, 'a', 'b', 'c', default=0)  # Returns 0
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


# Example usage when run directly
if __name__ == "__main__":
    # Test logging
    logger = setup_logging("test")
    logger.info("Logging is working!")
    
    # Test environment variable
    try:
        api_key = get_env_var("OPENAI_API_KEY", required=False)
        if api_key:
            logger.info("Environment variable loaded successfully")
        else:
            logger.info("No OPENAI_API_KEY found (this is okay for testing)")
    except ValueError as e:
        logger.error(f"Error: {e}")
    
    # Test retry
    def test_function():
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise Exception("Random failure")
        return "Success!"
    
    try:
        result = retry_with_exponential_backoff(test_function, max_attempts=5)
        logger.info(f"Retry test result: {result}")
    except Exception as e:
        logger.error(f"Retry test failed: {e}")
    
    print("\nUtils module is working correctly!")
