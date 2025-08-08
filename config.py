import os

from dotenv import load_dotenv

load_dotenv()

# Configuration constants for FAI OpenAPI
BASE_URL = os.getenv("FAI_BASE_URL", "https://client-open-api.stg.vnfai.com")
REALM = os.getenv("FAI_REALM", "aml")
CLIENT_ID = os.getenv("FAI_CLIENT_ID", "92d2b08f-0568-478f-99ec-b5fa7988b33c")
CLIENT_SECRET = os.getenv("FAI_CLIENT_SECRET", "3cc09597-7709-481d-a276-8d72fc0195f2")
GRANT_TYPE = "client_credentials"
