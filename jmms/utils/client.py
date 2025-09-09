from httpx import AsyncClient, ConnectTimeout, HTTPStatusError, RequestError, Response


async def get_data(
    url: str,
    headers: dict[str, str],
    proxy: str,
    timeout: int = None,
    attempts: int = 3,
) -> Response | None:
    """Fetch data from a given URL asynchronously with retry logic.

    Creates an ``httpx.AsyncClient`` with the given headers and proxy,
    then attempts to retrieve the response. Automatically retries
    on connection errors, timeouts, and HTTP status errors (4xx/5xx).

    Args:
        url (str): The target URL to request.
        headers (dict[str, str]): HTTP request headers.
        proxy (str): Proxy URL (e.g., "http://localhost:8080").
        timeout (int, optional): Request timeout in seconds. Defaults to None.
        attempts (int, optional): Number of retry attempts before failing. Defaults to 3.

    Returns:
        Response | None:
            - An ``httpx.Response`` object if the request succeeds.
            - ``None`` if all attempts fail.
              **Callers should check for ``None`` before accessing response attributes.**

    Raises:
        HTTPStatusError: If the server responds with a 4xx/5xx status and retries are exhausted.
        ConnectTimeout: If the request times out and retries are exhausted.
        RequestError: For other networking-related issues after retries.
    """
    client = AsyncClient(proxy=proxy, headers=headers, follow_redirects=True)

    async with client:
        for attempt in range(attempts):
            try:
                response = await client.get(url, timeout=timeout)

                # Raise error for 4xx & 5xx
                response.raise_for_status()

                return response
            except HTTPStatusError as e:
                print(
                    f"Attempt {attempt + 1}: Received {e.response.status_code} - Retrying..."
                )
            except (ConnectTimeout, RequestError):
                print("Network error occurred - Retrying...")
            except Exception as e:
                print(f"Something went wrong: {e}")

    print("All attempts failed, returning None")
    return None
