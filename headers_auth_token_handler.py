# UC6 – Configure Request Headers and Authentication

import requests
from typing import Dict, Any


class AuthenticatedApiClient:
    """
    HTTP client with header configuration and token-based authentication.
    """

    def __init__(self, base_url: str, token: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _build_headers(self) -> Dict[str, str]:
        """
        Construct request headers with authentication.
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def get_secure_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Send authenticated GET request.

        :param endpoint: API endpoint
        :return: JSON response
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._build_headers()

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)

            self._log_response(response, url)

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Connection failed")
        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] HTTP error: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"[ERROR] Unexpected error: {err}")

        return {}

    @staticmethod
    def _log_response(response: requests.Response, url: str) -> None:
        """
        Log response metadata.
        """
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Headers Sent: {response.request.headers}")


def main() -> None:
    # In real-world, use env variables or secrets manager
    token = "your_secure_token_here"

    client = AuthenticatedApiClient(
        base_url="https://jsonplaceholder.typicode.com",
        token=token
    )

    data = client.get_secure_data("/posts")

    if data:
        print("\n[INFO] Authenticated Request Successful")
        print(f"Fetched {len(data)} records")


if __name__ == "__main__":
    main()