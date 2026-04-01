# UC8 – Implement Robust Error and Exception Handling

import requests
import time
from typing import Dict, Any, List


class ResilientApiClient:
    """
    HTTP client with robust error handling and retry mechanism.
    """

    def __init__(self, base_url: str, timeout: int = 5, retries: int = 3) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

    def fetch_data(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Fetch data with retry and exception handling.
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(1, self.retries + 1):
            try:
                print(f"[INFO] Attempt {attempt} → {url}")

                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()

                return self._parse_json(response)

            except requests.exceptions.Timeout:
                print(f"[ERROR] Timeout on attempt {attempt}")
            except requests.exceptions.ConnectionError:
                print(f"[ERROR] Connection error on attempt {attempt}")
            except requests.exceptions.HTTPError as http_err:
                print(f"[ERROR] HTTP error: {http_err}")
                break  # No retry for HTTP errors
            except ValueError:
                print("[ERROR] Invalid JSON response")
                break
            except requests.exceptions.RequestException as err:
                print(f"[ERROR] Unexpected error: {err}")
                break

            time.sleep(2)  # Backoff before retry

        print("[FAILURE] All retry attempts failed")
        return []

    @staticmethod
    def _parse_json(response: requests.Response) -> List[Dict[str, Any]]:
        """
        Safely parse JSON response.
        """
        try:
            return response.json()
        except ValueError:
            raise ValueError("Response is not valid JSON")


def main() -> None:
    client = ResilientApiClient("https://jsonplaceholder.typicode.com")

    data = client.fetch_data("/posts")

    if data:
        print("\n[INFO] Data fetched successfully")
        print(f"Records: {len(data)}")
    else:
        print("[INFO] No data retrieved")


if __name__ == "__main__":
    main()