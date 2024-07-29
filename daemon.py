import json
import pickle
import re
import time
import os

import requests
from keep_alive import keep_alive  # Import the keep_alive function

COOKIES_FILE = 'cookies.txt'
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


def login():
    url = "https://faucetearner.org/api.php?act=login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://faucetearner.org",
        "Dnt": "1",
        "Referer": "https://faucetearner.org/login.php",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
        "Te": "trailers"
    }
    data = {
        "email": EMAIL,
        "password": PASSWORD
    }

    with requests.Session() as session:
        response = session.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data["code"] == 0:
                print("Login successful")
                # Save cookies using pickle
                with open(COOKIES_FILE, 'wb') as f:
                    pickle.dump(session.cookies, f)
                return True
            else:
                print("Login failed:", response_data["message"])
                return False
        else:
            print(f"Failed to login: HTTP {response.status_code} - {response.text}")
            return False


def faucet(session):  # Take the session object as an argument
    url = "https://faucetearner.org/api.php?act=faucet"
    headers = {  # (Same as login headers)
        # ...
    }

    response = session.post(url, headers=headers, json={})  # Use the existing session object
    if response.status_code == 200:
        response_data = response.json()
        print("Response:", json.dumps(response_data))
        if response_data["code"] == 0:
            match = re.search(
                r'<span translate=\'no\' class=\'text-info fs-2\'>(.+?)<\/span>',
                response_data["message"],
            )
            amount = match.group(1) if match else "unknown amount"
            print(f"Request successful: Received {amount}")
            return True
        elif response_data["code"] == 2:
            print("Wave missed:", response_data["message"])
            return False
    else:
        print(f"Failed to request: HTTP {response.status_code} - {response.text}")
        return False


# Login once and get the cookies
keep_alive()
if not login():
    print("Exiting due to failed login.")
else:  # Proceed only if login is successful
    with requests.Session() as session:
        # Load cookies using pickle
        with open(COOKIES_FILE, 'rb') as f:
            session.cookies.update(pickle.load(f))
        while True:
            if not faucet(session):  # Pass the session object to faucet()
                time.sleep(60)  # Wait before retrying
            else:
                time.sleep(60)  # Wait after a successful claim
