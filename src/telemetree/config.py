import requests
from src.telemetree import constants
from src.telemetree.exceptions import WrongIdentityKeys
from src.telemetree.telemetree_schemas import BotTrackingConfig



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

    def __init__(
        self,
        api_key: str,
        project_id: str,
    ) -> None:
        self.project_id = project_id
        self.api_key = api_key
        self.config = self.__get_config()

    def __get_config(self) -> dict:
        """
        Get the encryption keys from the Telemetree configuration service.

        Args:
            project_id (str): The project ID.
            api_key (str): The API key.

        Returns:
            dict: The encryption keys.
        """

        url = f"https://config.ton.solutions/v1/client/config?project={self.project_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers, timeout=constants.HTTP_TIMEOUT)

        response_json = response.json()
        if response.status_code != 200:
            raise WrongIdentityKeys(
                f"Failed to fetch the config. Status code: {response.status_code}. Response: {response_json}"
            )

        config = BotTrackingConfig(**response_json)

        return config

    def set_api_key(self, api_key: str) -> None:
        """
        Set the API key.

        Args:
            api_key (str): The API key.
        """
        self.api_key = api_key

    def set_project_id(self, project_id: str) -> None:
        """
        Set the project ID.

        Args:
            project_id (str): The project ID.
        """
        self.project_id = project_id

    def get_credentials(self) -> dict:
        """
        Get the API key and the project ID.

        Returns:
            dict: The API key and the project ID.
        """
        return {"API Key": self.api_key, "Project ID": self.project_id}
