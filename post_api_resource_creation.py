# UC3 – Create Resources via POST API

import requests
from typing import Dict, Any


class PostApiClient:
    """
    HTTP client for creating resources via POST API.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def create_resource(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send POST request with JSON payload.

        :param endpoint: API endpoint (e.g., /posts)
        :param payload: JSON data to send
        :return: Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)

            self._log_response(response, url)

            # Validate successful creation
            if response.status_code != 201:
                print(f"[WARNING] Unexpected status code: {response.status_code}")

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
        print(f"[DEBUG] Response Body: {response.text}")


def main() -> None:
    client = PostApiClient("https://jsonplaceholder.typicode.com")

    payload = {
        "title": "Senior Dev API",
        "body": "Creating resource via POST",
        "userId": 101
    }

    result = client.create_resource("/posts", payload)

    if result:
        print("\n[INFO] Resource Created:")
        print(result)


if __name__ == "__main__":
    main()