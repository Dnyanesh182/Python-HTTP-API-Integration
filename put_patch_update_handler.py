# UC4 – Update Resources using PUT/PATCH

import requests
from typing import Dict, Any


class UpdateApiClient:
    """
    HTTP client for updating resources using PUT and PATCH methods.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def update_full(self, endpoint: str, resource_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform full update using PUT.
        """
        url = f"{self.base_url}{endpoint}/{resource_id}"
        return self._send_request("PUT", url, payload)

    def update_partial(self, endpoint: str, resource_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform partial update using PATCH.
        """
        url = f"{self.base_url}{endpoint}/{resource_id}"
        return self._send_request("PATCH", url, payload)

    def _send_request(self, method: str, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )

            self._log_response(response, method, url)

            if response.status_code != 200:
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
    def _log_response(response: requests.Response, method: str, url: str) -> None:
        """
        Log response details.
        """
        print(f"[DEBUG] Method: {method}")
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Response Body: {response.text}")


def main() -> None:
    client = UpdateApiClient("https://jsonplaceholder.typicode.com")

    # PUT (Full Update)
    put_payload = {
        "id": 1,
        "title": "Fully Updated Title",
        "body": "Updated body content",
        "userId": 1
    }

    put_result = client.update_full("/posts", 1, put_payload)

    # PATCH (Partial Update)
    patch_payload = {
        "title": "Partially Updated Title"
    }

    patch_result = client.update_partial("/posts", 1, patch_payload)

    print("\n[INFO] PUT Response:", put_result)
    print("[INFO] PATCH Response:", patch_result)


if __name__ == "__main__":
    main()