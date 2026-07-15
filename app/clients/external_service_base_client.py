import httpx


class BaseClient:

    def post(
        self,
        endpoint: str,
        payload: dict,
        timeout: int = 30,
    ):

        response = httpx.post(
            endpoint,
            json=payload,
            timeout=timeout,
        )

        response.raise_for_status()

        if response.content:
            return response.json()

        return None