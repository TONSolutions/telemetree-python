import json
from enum import Enum
from socket import timeout
from typing import Optional
from urllib import request, error

from src.telemetree.constants import JSON_HEADER, HTTP_TIMEOUT


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
    """
    A class for making HTTP requests.

    Attributes:
        None

    Methods:
        get: Sends an HTTP GET request to the specified URL.
        post: Sends a POST request to the specified URL with the given data and headers.
    """

    @staticmethod
    def get(url: str, headers: Optional[dict] = None):
        """
        Sends an HTTP GET request to the specified URL.

        Args:
            url (str): The URL to send the GET request to.
            headers (Optional[dict]): Optional headers to include in the request.

        Returns:
            HTTPResponse: The response object returned by the server.

        Raises:
            HTTPError: If an HTTP error occurs.
            URLError: If a URL error occurs.
            timeout: If the request times out.
        """
        try:
            if not headers:
                req = request.Request(url, headers=JSON_HEADER)
            else:
                req = request.Request(url, headers=headers)

            resp = request.urlopen(req, timeout=HTTP_TIMEOUT)
            return resp

        except (error.HTTPError, error.URLError, timeout) as e:
            print(f"Error: {e}")
            raise e

    @staticmethod
    def post(url: str, data: dict, headers: Optional[dict] = None):
        """
        Sends a POST request to the specified URL with the given data and headers.

        Args:
            url (str): The URL to send the POST request to.
            data (dict): The data to be sent in the request body.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.

        Returns:
            HTTPResponse: The response object returned by the server.

        Raises:
            HTTPError: If an HTTP error occurs during the request.
            URLError: If a URL error occurs during the request.
            timeout: If the request times out.
        """
        try:
            if not headers:
                req = request.Request(url, headers=JSON_HEADER)
            else:
                req = request.Request(url, headers=headers)

            data = json.dumps(data).encode("utf-8")
            resp = request.urlopen(req, data, timeout=HTTP_TIMEOUT)
            return resp

        except (error.HTTPError, error.URLError, timeout) as e:
            print(f"Error: {e}")
            raise e
