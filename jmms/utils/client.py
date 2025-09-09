from httpx import AsyncClient, ConnectTimeout, RequestError, HTTPStatusError, Response


async def get_data(url: str, headers: dict[str, str], proxy: str, timeout: int = None, attempts: int = 3) -> None | Response:
    client = AsyncClient(proxy=proxy, headers=headers, follow_redirects=True)

    response = None
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
                print(f"Something went wrong {e}")

    print("All Attempts failed...")

    return response
