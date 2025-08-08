import base64
import hashlib
import hmac

from config import CLIENT_SECRET


def generateSignature(
    method: str,
    request_id: str,
    timestamp: str,
    content_md5: str,
    path: str,
    query_string: str,
):
    """Generate an X-Signature for an API request using HMAC-SHA256.

    The query string is appended to the path (same line) if it exists.
    """
    # Ensure empty strings for missing values
    content_md5 = content_md5 or ""
    query_string = query_string or ""

    # Append query string to path if present
    if query_string:
        path_with_query = f"{path}?{query_string}"
    else:
        path_with_query = path

    # Build signature message (5 lines total)
    signature_message = "\n".join(
        [method.upper(), request_id, timestamp, content_md5, path_with_query]
    )

    print(f"Signature Message (for HMAC):\n{signature_message}\n")

    # HMAC-SHA256 with Client Secret
    secret_bytes = CLIENT_SECRET.encode("utf-8")
    signature_bytes = signature_message.encode("utf-8")
    signature_hash = hmac.new(secret_bytes, signature_bytes, hashlib.sha256).digest()

    return base64.b64encode(signature_hash).decode("utf-8")
