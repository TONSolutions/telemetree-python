from enum import Enum
from socket import timeout
import logging
from uuid import UUID
from typing import Optional

import requests

from telemetree.schemas.constants import HTTP_TIMEOUT
from telemetree.core.config import Config
from telemetree.schemas.telemetree_schemas import EncryptedEvent

logger = logging.getLogger("telemetree.http_client")


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
    def __init__(self, ads_user_id: UUID, settings: Optional[Config] = None) -> None:
        # self.settings = settings
        # self.url = self.settings.config.host
        # self.api_key = self.settings.api_key
        # self.project_id = self.settings.project_id
        self.ads_user_id = ads_user_id

    def post(self, data: EncryptedEvent):
        """
        Sends a POST request to the specified URL with the given data and headers.

        Args:
            data (EncryptedEvent): The data to be sent in the request body.

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

            data = data.model_dump_json()

            request = requests.post(
                self.url, json=data, headers=headers, timeout=HTTP_TIMEOUT
            )

            return request

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
            timeout,
        ) as e:
            logger.exception("Failed to send POST request: %s", e)
            raise e

    def get(self, url: str, query_params: Optional[dict] = None):
        """
        Sends a GET request to the specified URL with the given headers.

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
                "ads-user-id": self.ads_user_id,
            }
            request = requests.get(
                url, headers=headers, timeout=HTTP_TIMEOUT, params=query_params
            )

            request.raise_for_status()

            return request

        except (
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as e:
            logger.exception("Failed to send GET request: %s", e)
            raise e
