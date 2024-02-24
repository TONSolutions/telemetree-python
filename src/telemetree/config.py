import requests
from telemetree import constants

# Don't forget to add env variables


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

    def __init__(self, project_id, api_key) -> dict:
        self.project_id = project_id
        self.api_key = api_key
        self.encryption_keys = self.get_encryption_keys(project_id, api_key)

    def get_encryption_keys(self, project_id, api_key):
        """
        Get the encryption keys from the Telemetree configuration service.

        Args:
            project_id (str): The project ID.
            api_key (str): The API key.

        Returns:
            dict: The encryption keys.
        """

        url = f"https://config.ton.solutions/v1/client/config?project={project_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers, timeout=constants.HTTP_TIMEOUT)
        return response.json()
