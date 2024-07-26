import json
import pickle
import re
import time
import os
import requests

# Define your credentials directly
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
COOKIES_FILE = 'cookies.txt'


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
        try:
            response = session.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            if response.text:
                try:
                    response_data = response.json()
                    if response_data.get("code") == 0:
                        print("Login successful")
                        # Save cookies using pickle
                        with open(COOKIES_FILE, 'wb') as f:
                            pickle.dump(session.cookies, f)
                        return True
                    else:
                        print("Login failed:", response_data.get("message", "No message in response"))
                        return False
                except json.JSONDecodeError:
                    print("Error decoding JSON from response")
                    print(f"Response Text: {response.text}")
                    return False
            else:
                print("Empty response received")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Failed to login: {e}")
            return False


def faucet(session):  # Take the session object as an argument
    url = "https://faucetearner.org/api.php?act=faucet"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://faucetearner.org",
        "Dnt": "1",
        "Referer": "https://faucetearner.org/faucet.php",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
        "Te": "trailers"
    }

    try:
        response = session.post(url, headers=headers, json={})
        response.raise_for_status()  # Raise an HTTPError for bad responses
        if response.text:
            try:
                response_data = response.json()
                print("Response:", json.dumps(response_data, indent=4))
                if response_data.get("code") == 0:
                    match = re.search(
                        r'<span translate=\'no\' class=\'text-info fs-2\'>(.+?)<\/span>',
                        response_data.get("message", ""),
                    )
                    amount = match.group(1) if match else "unknown amount"
                    print(f"Request successful: Received {amount}")
                    return True
                elif response_data.get("code") == 2:
                    print("Wave missed:", response_data.get("message", "No message in response"))
                    return False
            except json.JSONDecodeError:
                print("Error decoding JSON from response")
                print(f"Response Text: {response.text}")
                return False
        else:
            print("Empty response received")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to request: {e}")
        return False


# Login once and get the cookies
if not login():
    print("Exiting due to failed login.")
else:  # Proceed only if login is successful
    with requests.Session() as session:
        # Load cookies using pickle
        try:
            with open(COOKIES_FILE, 'rb') as f:
                session.cookies.update(pickle.load(f))
        except (FileNotFoundError, pickle.PickleError) as e:
            print(f"Error loading cookies: {e}")
            print("Exiting due to cookie loading failure.")
            exit(1)

        while True:
            if not faucet(session):  # Pass the session object to faucet()
                time.sleep(60)  # Wait before retrying
            else:
                time.sleep(60)  # Wait after a successful claim
