# UC1 – Implement HTTP GET Request Client

import requests
from typing import Any, Dict, List


class HttpGetClient:
    """
    Reusable HTTP client for performing GET requests.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Execute GET request and return parsed JSON response.

        :param endpoint: API endpoint (e.g., /posts)
        :return: List of JSON objects
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, timeout=self.timeout)

            # Debug logging
            self._log_response(response, url)

            # Validate response
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

        return []

    @staticmethod
    def _log_response(response: requests.Response, url: str) -> None:
        """
        Internal helper for logging response metadata.
        """
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type')}")


def main() -> None:
    client = HttpGetClient("https://jsonplaceholder.typicode.com")

    data = client.fetch("/posts")

    if data:
        print("\n[INFO] Sample Output:")
        for item in data[:3]:
            print(f"ID: {item['id']} | Title: {item['title']}")


if __name__ == "__main__":
    main()