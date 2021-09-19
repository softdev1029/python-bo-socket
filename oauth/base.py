from base.logger import log
import requests

# from .utils import Client

API_URL = "http://api.crmd.bo.market"

TOKEN_URL = API_URL + "/o/token/"
LOGIN_URL = API_URL + "/login"
API_URL = API_URL + "/oauth/apikeys/"


def get_access_token():
    log("Getting access token from", TOKEN_URL, "...")
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic dnA0Sk9XWHk1b1M2OG9TbkRwcklxVTNnMVE4VnlNVEFPaEZ4VjdGdzpqV1k3Mjl0dTNJZ1MwSkpITWw0bk9aTjZvR2lMZFZxQVQ0cjg4YWJTY2F1c3d3V1FZa0lIM2hRQjQxVkFzT0hQdEtOMEM1Mm1LV21xcGdIZ1Fzanp3TEp5OEZ6ZWFUT3hQNTFpMUlJSk5kM1NJcTJ0eGVvVHlGSUFjOEFlTHFyRg=="
        },
    )
    try:
        return response.json()["access_token"]
    except Exception as e:
        print(e)
        return ""


def get_session_token(email, password):
    log("Getting session token ...")
    response = requests.post(
        LOGIN_URL,
        data={
            "method": "email",
            "email": email,
            "password": password,
            "code": "",
        },
    )
    try:
        return response.json()["data"]["sessionToken"]
    except Exception as e:
        print(e)
        return ""


def get_api_keys():
    email = input("Enter email: ")
    password = input("Enter password: ")

    access_token = get_access_token()
    log("Access Token is", access_token)

    session_token = get_session_token(email, password)
    log("Session Token is", session_token)

    if access_token and session_token:
        key_uri = API_URL + session_token
        auth_head = "Bearer " + access_token

        log("Getting API key ...")
        response = requests.get(key_uri, headers={"Authorization": auth_head})
        try:
            log("API Key is", response.text)
            return response.text
        except Exception as e:
            print(e)
            return ""
    log("API Key can't be fetched because of invalid credential")
    return ""
