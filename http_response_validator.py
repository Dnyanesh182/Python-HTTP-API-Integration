# UC7 – Validate HTTP Responses and Metadata

import requests
from typing import Dict, Any, List


class ResponseValidator:
    """
    Validates HTTP response status, headers, and payload integrity.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def fetch_and_validate(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Fetch API data and validate response.
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, timeout=self.timeout)

            self._log_response(response, url)

            self._validate_status(response)
            self._validate_headers(response)
            data = self._validate_payload(response)

            return data

        except ValueError as val_err:
            print(f"[VALIDATION ERROR] {val_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"[REQUEST ERROR] {req_err}")

        return []

    @staticmethod
    def _validate_status(response: requests.Response) -> None:
        if not (200 <= response.status_code < 300):
            raise ValueError(f"Invalid status code: {response.status_code}")

    @staticmethod
    def _validate_headers(response: requests.Response) -> None:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError(f"Invalid Content-Type: {content_type}")

    @staticmethod
    def _validate_payload(response: requests.Response) -> List[Dict[str, Any]]:
        try:
            data = response.json()
        except ValueError:
            raise ValueError("Response is not valid JSON")

        if not isinstance(data, list) or not data:
            raise ValueError("Invalid or empty payload")

        # Validate structure of first item
        required_keys = {"id", "title"}
        if not required_keys.issubset(data[0].keys()):
            raise ValueError("Payload structure mismatch")

        return data

    @staticmethod
    def _log_response(response: requests.Response, url: str) -> None:
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Content-Type: {response.headers.get('Content-Type')}")


def main() -> None:
    validator = ResponseValidator("https://jsonplaceholder.typicode.com")

    data = validator.fetch_and_validate("/posts")

    if data:
        print("\n[INFO] Validation Successful")
        print(f"Records fetched: {len(data)}")


if __name__ == "__main__":
    main()