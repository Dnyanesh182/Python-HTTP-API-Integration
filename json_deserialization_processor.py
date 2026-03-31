# UC2 – Deserialize and Process JSON Responses

from typing import List, Dict, Any


class JsonProcessor:
    """
    Handles JSON deserialization and data extraction.
    """

    @staticmethod
    def extract_posts(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract relevant fields from JSON response.

        :param data: Raw JSON list
        :return: Processed list with selected fields
        """
        processed_data = []

        for item in data:
            try:
                processed_data.append({
                    "id": item["id"],
                    "title": item["title"]
                })
            except KeyError as e:
                print(f"[WARNING] Missing key: {e}")

        return processed_data

    @staticmethod
    def display(data: List[Dict[str, Any]]) -> None:
        """
        Display processed data.
        """
        print("\n[INFO] Processed Output:")
        for item in data[:3]:
            print(f"ID: {item['id']} | Title: {item['title']}")


def main() -> None:
    # Sample input (simulating API response)
    sample_data = [
        {"id": 1, "title": "Post One", "body": "Content"},
        {"id": 2, "title": "Post Two", "body": "Content"},
        {"id": 3, "title": "Post Three"}  # Missing optional fields handled safely
    ]

    processor = JsonProcessor()
    extracted = processor.extract_posts(sample_data)
    processor.display(extracted)


if __name__ == "__main__":
    main()