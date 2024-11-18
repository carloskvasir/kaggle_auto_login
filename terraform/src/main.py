"""
Kaggle Auto Login Cloud Function.

This function automates the login process to Kaggle to maintain activity streak.
It uses environment variables for authentication and provides streak information.
"""

import os
import logging
import requests
import functions_framework
from typing import Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%03d'
)
logger = logging.getLogger(__name__)

def get_xsrf_token(session: requests.Session) -> str:
    """
    Get XSRF token from Kaggle.
    
    Args:
        session: The requests session object
    
    Returns:
        str: XSRF token
    """
    response = session.get('https://www.kaggle.com/account/login')
    response.raise_for_status()
    
    # Extract XSRF token from cookies
    xsrf_token = session.cookies.get('XSRF-TOKEN')
    if not xsrf_token:
        raise ValueError("Failed to get XSRF token")
    
    return xsrf_token

def perform_login(session: requests.Session, xsrf_token: str, email: str, password: str) -> None:
    """
    Perform login to Kaggle.
    
    Args:
        session: The requests session object
        xsrf_token: XSRF token for authentication
        email: Kaggle account email
        password: Kaggle account password
    """
    headers = {
        'x-xsrf-token': xsrf_token,
        'content-type': 'application/json',
    }
    
    data = {
        'username': email,
        'password': password,
        'keepMeSignedIn': False
    }
    
    response = session.post(
        'https://www.kaggle.com/api/v1/users/LegacyUsersService/EmailSignIn',
        headers=headers,
        json=data
    )
    response.raise_for_status()

def verify_login_success(session: requests.Session, xsrf_token: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Verify if login was successful and get activity stats.
    
    Args:
        session: The requests session object
        xsrf_token: XSRF token for authentication
    
    Returns:
        Tuple[bool, dict]: Success status and user stats
    """
    headers = {
        'x-xsrf-token': xsrf_token,
        'content-type': 'application/json',
    }
    
    # Visit home page to establish valid session
    response = session.get('https://www.kaggle.com')
    response.raise_for_status()
    
    # Get user stats
    response = session.get(
        'https://www.kaggle.com/api/v1/users/HomePageService/GetHomePageStats',
        headers=headers
    )
    response.raise_for_status()
    
    stats = response.json()
    return True, stats

@functions_framework.http
def kaggle_login(request) -> Tuple[str, int]:
    """
    Cloud Function entry point for Kaggle login.
    
    Args:
        request: Flask request object
    
    Returns:
        Tuple[str, int]: Response message and status code
    """
    try:
        # Get credentials from environment
        email = os.environ['KAGGLE_EMAIL']
        password = os.environ['KAGGLE_PASSWORD']
        
        # Initialize session
        session = requests.Session()
        
        # Get XSRF token
        logger.info("Getting XSRF token...")
        xsrf_token = get_xsrf_token(session)
        
        # Perform login
        logger.info("Performing login...")
        perform_login(session, xsrf_token, email, password)
        
        # Verify login success
        logger.info("Verifying login...")
        success, stats = verify_login_success(session, xsrf_token)
        
        if success:
            streak = stats.get('currentStreak', 0)
            logger.info(f"Login successful! Current streak: {streak} days")
            return f"Login successful! Current streak: {streak} days", 200
        else:
            logger.error("Login verification failed")
            return "Login verification failed", 500
            
    except KeyError as e:
        logger.error(f"Missing environment variable: {str(e)}")
        return f"Configuration error: Missing {str(e)}", 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return f"Request failed: {str(e)}", 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}", 500
