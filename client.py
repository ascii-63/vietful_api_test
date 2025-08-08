import hashlib
import json
import time
import uuid
from urllib.parse import urlencode

import requests

from auth import getAccessToken
from config import BASE_URL
from signature import generateSignature


class FAIAPIClient:
    """Generic client for making FAI OpenAPI requests."""

    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None

    def _get_headers(self, request_id, timestamp, content_md5, signature):
        """Generate common headers for API requests."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-RequestId": request_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "X-Content-MD5": content_md5,
            "Content-Type": "application/json",
        }
        return headers

    def _generate_content_md5(self, body: dict):
        """Generate MD5 hash of the request body."""
        if not body:
            return ""
        body = json.dumps(body, separators=(",", ":"))
        return hashlib.md5(body.encode("utf-8")).hexdigest().upper()

    def makeRequest(self, method, path, query_params=None, body=None):
        """Make an API request with the specified method, path, query parameters, and body.

        Args:
            method (str): HTTP method (e.g., GET, POST).
            path (str): API path (e.g., /api/v1/sorting-sessions/info/{location_code}).
            query_params (dict, optional): Query parameters.
            body (dict, optional): Request body for POST/PUT requests.

        Returns:
            dict: API response JSON or None if the request fails.
        """
        # Ensure access token is valid
        if not self.access_token:
            self.access_token = getAccessToken()
            if not self.access_token:
                print("Failed to get access token")
                return None

        # Prepare request components
        request_id = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))
        query_string = urlencode(query_params) if query_params else ""
        content_md5 = self._generate_content_md5(body if body else "")
        signature = generateSignature(
            method, request_id, timestamp, content_md5, path, query_string
        )

        # Build URL and headers
        url = f"{self.base_url}{path}" + (f"?{query_string}" if query_string else "")
        headers = self._get_headers(request_id, timestamp, content_md5, signature)

        try:
            print(f"Headers: {headers}\n")
            # print(f"RequestId: {headers.get('X-RequestId')}")
            print(f"Body: {body}\n")
            response = requests.request(method, url, headers=headers, json=body)
            response.raise_for_status()
            print(f"✅ {method} {path}: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"❌ {method} {path} failed: {error}")
            if hasattr(error, "response") and error.response is not None:
                print(f"Status Code: {error.response.status_code}")
                print(f"Response headers: {error.response.headers}")
                print(f"Response body: {error.response.text}")
            return None
