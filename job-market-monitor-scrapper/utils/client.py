import httpx
from httpx import RequestError


def get_data(url, headers, proxy, timeout=None, attempt=3):
    client = httpx.Client(proxy=proxy, headers=headers, follow_redirects=True)

    response = None
    with client:
        for attempt in range(attempt):
            try:
                if timeout:
                    response = client.get(url, timeout=timeout)
                else:
                    response = client.get(url)

                # Raise an error for bad status code
                if f"{response.status_code}".startswith(
                    "4"
                ) or f"{response.status_code}".startswith("5"):
                    response.raise_for_status()

                # Close tcp connection for successful result
                client.close()
                return response
            except httpx.HTTPStatusError as e:
                print(
                    f"Attempt {attempt + 1}: Received {e.response.status_code} - Retrying..."
                )
            except httpx.ConnectTimeout:
                print("Network error occurred - Retrying...")
            except Exception as e:
                print(f"Something went wrong {e}")

    print("All Attempts failed...")

    return response
