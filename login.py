# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

def load_env_variables():
    """
    Loads environment variables from the .env file.
    """
    load_dotenv()
    return os.getenv("EMAIL"), os.getenv("PASSWORD"), os.getenv("USER")

def get_xsrf_token(session):
    """
    Retrieves the XSRF token from the initial login page.
    """
    initial_response = session.get("https://www.kaggle.com/account/login")
    xsrf_token = session.cookies.get('XSRF-TOKEN')
    if not xsrf_token:
        # If the token is not in the cookies, look for it in the HTML page
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        xsrf_token_tag = soup.find('input', {'name': 'X-XSRF-TOKEN'})
        if xsrf_token_tag:
            xsrf_token = xsrf_token_tag['value']
    if not xsrf_token:
        raise Exception("Could not find the XSRF Token.")
    return xsrf_token

def login(session, email, password, user, xsrf_token):
    """
    Logs into Kaggle using email, password, and XSRF token.
    """
    login_url = 'https://www.kaggle.com/api/i/users.LegacyUsersService/EmailSignIn'
    login_data = {
        'email': email,
        'password': password,
        'returnUrl': f"/{user}"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Content-Type': 'application/json',
        'X-XSRF-TOKEN': xsrf_token
    }
    return session.post(login_url, json=login_data, headers=headers)

def access_edit_page(session, user, headers):
    """
    Accesses the edit page of a specific notebook.
    """
    edit_url = f"https://www.kaggle.com/code/{user}/exercise-syntax-variables-and-numbers/edit"
    return session.get(edit_url, headers=headers)

def main():
    """
    Main function that orchestrates the login process and access to the edit page.
    """
    email, password, user = load_env_variables()
    session = requests.Session()
    xsrf_token = get_xsrf_token(session)
    login_response = login(session, email, password, user, xsrf_token)
    
    if login_response.status_code == 200:
        print("[OK] Login successful.")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'Content-Type': 'application/json',
            'X-XSRF-TOKEN': xsrf_token
        }
        edit_response = access_edit_page(session, user, headers)
        if edit_response.status_code == 200:
            print("[OK] Edit page accessed successfully.")
        else:
            print(f"[ERROR] Error accessing the edit page. Status Code: {edit_response.status_code}")
            print(edit_response.text)
    else:
        print(f"[ERROR] Login failed. Status Code: {login_response.status_code}")
        print(f"Error message: {login_response.text}")

if __name__ == "__main__":
    main()
