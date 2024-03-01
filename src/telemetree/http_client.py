from enum import Enum
from socket import timeout
import requests

from src.telemetree.constants import HTTP_TIMEOUT
from src.telemetree.config import Config


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class HttpClient:
    def __init__(self, settings: Config) -> None:
        self.settings = settings
        self.url = self.settings.config.host
        self.api_key = self.settings.api_key
        self.project_id = self.settings.project_id

    def post(self, data: dict):
        """
        Sends a POST request to the specified URL with the given data and headers.

        Args:
            data (dict): The data to be sent in the request body.

        Returns:
            HTTPResponse: The response object returned by the server.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
            URLError: If a URL error occurs during the request.
            timeout: If the request times out.
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "x-project-id": self.project_id,
            }

            request = requests.post(
                self.url, json=data, headers=headers, timeout=HTTP_TIMEOUT
            )

            return request

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
            timeout,
        ) as e:
            print(f"Error: {e}")
            raise e
