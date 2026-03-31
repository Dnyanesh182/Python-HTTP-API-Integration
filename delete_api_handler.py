# UC5 – Perform Resource Deletion via HTTP DELETE

import requests


class DeleteApiClient:
    """
    HTTP client for deleting resources via DELETE API.
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def delete_resource(self, endpoint: str, resource_id: int) -> bool:
        """
        Perform DELETE request for a given resource.

        :param endpoint: API endpoint (e.g., /posts)
        :param resource_id: ID of resource to delete
        :return: True if deletion successful, else False
        """
        url = f"{self.base_url}{endpoint}/{resource_id}"

        try:
            response = requests.delete(url, timeout=self.timeout)

            self._log_response(response, url)

            if response.status_code in (200, 204):
                print("[INFO] Resource deleted successfully")
                return True
            else:
                print(f"[WARNING] Unexpected status code: {response.status_code}")

            response.raise_for_status()

        except requests.exceptions.Timeout:
            print("[ERROR] Request timed out")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Connection failed")
        except requests.exceptions.HTTPError as http_err:
            print(f"[ERROR] HTTP error: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"[ERROR] Unexpected error: {err}")

        return False

    @staticmethod
    def _log_response(response: requests.Response, url: str) -> None:
        """
        Log response details.
        """
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Status Code: {response.status_code}")


def main() -> None:
    client = DeleteApiClient("https://jsonplaceholder.typicode.com")

    success = client.delete_resource("/posts", 1)

    if success:
        print("[INFO] Deletion verified")
    else:
        print("[INFO] Deletion failed")


if __name__ == "__main__":
    main()