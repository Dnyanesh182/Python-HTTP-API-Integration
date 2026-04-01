# UC10 – Build End-to-End API Integration Workflow

import requests
from typing import List, Dict, Any


class ApiIntegrationPipeline:
    """
    End-to-end API pipeline: request → validate → parse → filter → output
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def execute(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Execute full API pipeline.
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, timeout=self.timeout)

            self._log_response(response, url)

            self._validate_response(response)

            data = self._parse_json(response)

            filtered_data = self._filter_data(data)

            return filtered_data

        except requests.exceptions.RequestException as err:
            print(f"[ERROR] API request failed: {err}")

        return []

    @staticmethod
    def _validate_response(response: requests.Response) -> None:
        if not (200 <= response.status_code < 300):
            raise ValueError(f"Invalid status code: {response.status_code}")

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise ValueError("Invalid Content-Type")

    @staticmethod
    def _parse_json(response: requests.Response) -> List[Dict[str, Any]]:
        try:
            return response.json()
        except ValueError:
            raise ValueError("Invalid JSON response")

    @staticmethod
    def _filter_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Business logic: filter posts with userId = 1
        """
        return [
            {"id": item["id"], "title": item["title"]}
            for item in data
            if item.get("userId") == 1
        ]

    @staticmethod
    def _log_response(response: requests.Response, url: str) -> None:
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")

    @staticmethod
    def display(data: List[Dict[str, Any]]) -> None:
        print("\n[INFO] Processed Output:")
        for item in data[:5]:
            print(f"ID: {item['id']} | Title: {item['title']}")


def main() -> None:
    pipeline = ApiIntegrationPipeline("https://jsonplaceholder.typicode.com")

    result = pipeline.execute("/posts")

    if result:
        pipeline.display(result)
        print(f"\n[INFO] Total Filtered Records: {len(result)}")
    else:
        print("[INFO] No data processed")


if __name__ == "__main__":
    main()