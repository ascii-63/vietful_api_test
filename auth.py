import time
import uuid

import requests

from config import BASE_URL, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE, REALM


def getAccessToken():
    """Retrieve an OAuth 2.0 access token from the FAI OpenAPI authentication endpoint.

    Returns:
        str: Access token if successful, None otherwise.
    """
    token_path = f"/auth/realms/{REALM}/protocol/openid-connect/token"
    url = f"{BASE_URL}{token_path}"

    body_data = {
        "grantType": GRANT_TYPE,
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "refreshToken": "",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RequestId": str(uuid.uuid4()),
        "X-Timestamp": str(int(time.time() * 1000)),
    }

    try:
        response = requests.post(url, data=body_data, headers=headers)
        response.raise_for_status()
        print("✅ Access Token retrieved successfully.\n")
        return response.json().get("accessToken")
    except requests.exceptions.RequestException as error:
        print(f"❌ Error getting access token: {error}")
        if hasattr(error, "response") and error.response is not None:
            print(f"Response: {error.response.text}")
        return None
