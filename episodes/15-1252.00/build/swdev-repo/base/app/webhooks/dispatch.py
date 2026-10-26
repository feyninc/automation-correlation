"""POST one webhook event to one tenant endpoint and record the result."""
from dataclasses import dataclass

import requests

RESPONSE_SNIPPET_BYTES = 4096  # kept on the delivery row for the dashboard's "Response" column
TIMEOUT = (3.05, 10)  # connect, read (seconds)


@dataclass
class DeliveryResult:
    status: int
    snippet: bytes


def post_event(url: str, body: bytes, headers: dict[str, str]) -> DeliveryResult:
    """url is the tenant's configured endpoint (any public https URL)."""
    with requests.post(url, data=body, headers=headers, timeout=TIMEOUT, stream=True) as resp:
        snippet = b""
        for chunk in resp.iter_content(chunk_size=1024):
            snippet += chunk
            if len(snippet) >= RESPONSE_SNIPPET_BYTES:
                break
    return DeliveryResult(status=resp.status_code, snippet=snippet[:RESPONSE_SNIPPET_BYTES])


def deliver(event_id: str, endpoint_id: str) -> None:  # signs, posts, records, retries; omitted
    raise NotImplementedError
