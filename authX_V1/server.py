"""Python Flask WebApp Auth0 integration example
"""

from os import environ as env
import http.client
import json

from dotenv import find_dotenv, load_dotenv
from flask import Flask
import requests

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


@app.route("/get_token")
def get_token():
    conn = http.client.HTTPSConnection("dev-a1tb1w5yujx4tatj.us.auth0.com")

    client_id = env.get("AUTH0_CLIENT_ID")
    client_secret = env.get("AUTH0_CLIENT_SECRET")
    api_identifier = env.get("AUTH0_API_IDENTIFIER")
    payload = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&audience={api_identifier}"

    headers = {'content-type': "application/x-www-form-urlencoded"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read().decode('utf-8')
    return json.loads(data)


@app.route("/call_public_api")
def call_public_api():
    access_token = get_token()['access_token']
    print(access_token)

    headers = {
        'content-type': "application/json",
        'authorization': 'Bearer ' + access_token
    }

    res = requests.get("http://django-api:8000/api/public", headers)

    return res.text


@app.route("/call_private_api")
def call_private_api():
    access_token = get_token()['access_token']
    print(access_token)

    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    res = requests.get("http://django-api:8000/api/private", headers=headers)

    return res.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3010))
