import httpx
from httpx import RequestError, ConnectTimeout


def get_data(url, headers, proxy, timeout=None, attempts=3):
    client = httpx.Client(proxy=proxy, headers=headers, follow_redirects=True)

    response = None
    with client:
        for attempt in range(attempts):
            try:
                response = client.get(url, timeout=timeout)

                # Raise error for 4xx & 5xx
                response.raise_for_status()

                return response
            except httpx.HTTPStatusError as e:
                print(
                    f"Attempt {attempt + 1}: Received {e.response.status_code} - Retrying..."
                )
            except (ConnectTimeout, RequestError):
                print("Network error occurred - Retrying...")
            except Exception as e:
                print(f"Something went wrong {e}")

    print("All Attempts failed...")

    return response
