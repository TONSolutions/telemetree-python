import logging

from telemetree.schemas import TelemetreeConfig
from telemetree.http_client import HttpClient

logger = logging.getLogger("telemetree.config")


class Config:
    """
    Represents the configuration for Telemetree.

    Args:
        project_id (str): The project ID.
        api_key (str): The API key.

    Attributes:
        project_id (str): The project ID.
        api_key (str): The API key.
        encryption_keys (dict): The encryption keys obtained from the Telemetree configuration service.

    """

    CONFIG_URL = "https://config.ton.solutions/v1/client/config"

    def __init__(
        self,
        http_client: HttpClient,
    ) -> None:
        self.http_client = http_client
        self.config = self.__get_config()

    def __get_config(self) -> TelemetreeConfig:
        """
        Get the encryption keys from the Telemetree configuration service.

        Returns:
            TelemetreeConfig: The Telemetree configuration.
        """
        response = self.http_client.get(self.CONFIG_URL)

        return TelemetreeConfig(**response)

    def get_public_key(self) -> str:
        return self.config.public_key

    def get_host(self) -> str:
        return self.config.host
