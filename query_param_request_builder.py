# UC9 – Handle Query Parameters and Dynamic Requests

import requests
from typing import Dict, Any, List, Optional


class QueryApiClient:
    """
    HTTP client supporting dynamic query parameters.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_with_params(
        self,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Send GET request with dynamic query parameters.

        :param endpoint: API endpoint
        :param query_params: Dictionary of query params
        :return: JSON response list
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(
                url,
                params=query_params,
                timeout=self.timeout
            )

            self._log_request(url, query_params, response)

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
    def _log_request(url: str, params: Optional[Dict[str, Any]], response: requests.Response) -> None:
        """
        Log request and response details.
        """
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Query Params: {params}")
        print(f"[DEBUG] Final URL: {response.url}")
        print(f"[DEBUG] Status Code: {response.status_code}")


def main() -> None:
    client = QueryApiClient("https://jsonplaceholder.typicode.com")

    # Example: filter posts by userId
    params = {"userId": 1}

    data = client.fetch_with_params("/posts", params)

    if data:
        print("\n[INFO] Filtered Results:")
        for item in data[:3]:
            print(f"ID: {item['id']} | Title: {item['title']}")


if __name__ == "__main__":
    main()