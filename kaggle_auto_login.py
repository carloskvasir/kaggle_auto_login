"""
Kaggle Auto Login Script.

This script automates the login process to Kaggle to maintain activity streak.
It uses environment variables for authentication and provides streak information.
"""

import os
import logging
import requests
from typing import Tuple
from dotenv import load_dotenv

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%03d'
)
logger = logging.getLogger(__name__)

def login_to_kaggle(session: requests.Session, email: str, password: str) -> Tuple[bool, str]:
    """
    Login to Kaggle and get XSRF token.
    
    Args:
        session: requests Session object
        email: Kaggle account email
        password: Kaggle account password
        
    Returns:
        Tuple[bool, str]: Success status and XSRF token if successful
    """
    try:
        # Get initial XSRF token from login page
        logger.info("Getting initial XSRF token...")
        response = session.get('https://www.kaggle.com/account/login')
        response.raise_for_status()
        
        xsrf_token = session.cookies.get('XSRF-TOKEN')
        if not xsrf_token:
            logger.error("Could not find XSRF-TOKEN in initial cookies")
            return False, ""
            
        logger.info("Got initial XSRF token")
        
        # Perform login
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.kaggle.com',
            'referer': 'https://www.kaggle.com/account/login',
            'x-xsrf-token': xsrf_token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        data = {
            "email": email,
            "password": password,
            "keepMeSignedIn": False
        }
        
        logger.info("Attempting login...")
        response = session.post(
            'https://www.kaggle.com/api/i/users.LegacyUsersService/EmailSignIn',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        
        # Visit home page to establish valid session
        logger.info("Visiting home page...")
        response = session.get('https://www.kaggle.com')
        response.raise_for_status()
        
        # Get new XSRF token after login
        xsrf_token = session.cookies.get('XSRF-TOKEN')
        if not xsrf_token:
            logger.error("Could not find XSRF-TOKEN after login")
            return False, ""
            
        logger.info("Successfully logged in")
        return True, xsrf_token
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return False, ""

def verify_login_success(session: requests.Session, xsrf_token: str) -> Tuple[bool, dict]:
    """
    Verify if login was successful and get activity stats.

    Args:
        session: The requests session object
        xsrf_token: XSRF token for authentication

    Returns:
        Tuple[bool, dict]: Success status and user stats
    """
    try:
        # Get user ID
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://www.kaggle.com',
            'referer': 'https://www.kaggle.com/',
            'x-xsrf-token': xsrf_token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        data = {
            "includeGroups": False,
            "includeLogins": False,
            "includeVerificationStatus": True
        }
        
        logger.info("Getting user information...")
        response = session.post(
            'https://www.kaggle.com/api/i/users.UsersService/GetCurrentUser',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        
        user_data = response.json()
        user_id = user_data.get('id')
        
        if not user_id:
            logger.error("Could not get user ID")
            return False, {}
            
        # Get user stats
        logger.info("Getting user stats...")
        response = session.post(
            'https://www.kaggle.com/api/i/users.HomePageService/GetHomePageStats',
            json={"userId": user_id},
            headers=headers
        )
        response.raise_for_status()
        
        return True, response.json()
        
    except Exception as e:
        logger.error(f"Failed to verify login: {str(e)}")
        return False, {}

def main():
    """Main function to run the Kaggle login script."""
    try:
        # Load environment variables
        load_dotenv()
        email = os.getenv('KAGGLE_EMAIL')
        password = os.getenv('KAGGLE_PASSWORD')

        if not all([email, password]):
            logger.error("Missing required environment variables (KAGGLE_EMAIL, KAGGLE_PASSWORD)")
            return

        # Create session and login
        session = requests.Session()
        success, xsrf_token = login_to_kaggle(session, email, password)
        if not success:
            logger.error("Login failed")
            return

        # Verify login and get streak info
        success, stats = verify_login_success(session, xsrf_token)
        if not success:
            logger.error("Failed to verify login")
            return

        # Print streak information
        current_streak = stats.get('currentDayStreak', 0)
        max_streak = stats.get('maxDayStreak', 0)
        logger.info(f"Login successful! Current streak: {current_streak}, Max streak: {max_streak}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
