import json
import logging
from typing import Optional

from telemetree.config import Config
from telemetree.http_client import HttpClient
from telemetree.telemetree_schemas import EncryptedEvent
from telemetree.encryption import EncryptionService
from telemetree.event_builder import EventBuilder
from telemetree.orchestrator import orchestrate_event
from telemetree.utils import convert_public_key


logger = logging.getLogger("telemetree.client")


class TelemetreeClient:
    def __init__(self, api_key: str, project_id: str):
        """
        Initializes the TelemetreeClient with the provided API key and project ID.

        Args:
            api_key (str): The API key for authentication.
            project_id (str): The project ID for the Telemetree service.
        """
        self.api_key = api_key
        self.project_id = project_id

        self.settings = Config(self.api_key, self.project_id)

        self.public_key = convert_public_key(self.settings.config.public_key)

        self.encryption_service = EncryptionService(self.public_key)
        self.http_client = HttpClient(self.settings)
        self.event_builder = EventBuilder(self.settings)

    def track(self, event: dict) -> Optional[int]:
        """
        Tracks a Telegram update event.

        Args:
            event (dict): The Telegram update event to track.

        Returns:
            Optional[int]: The status code of the HTTP response if the event was tracked successfully, None otherwise.
        """
        try:
            orchestrated_event = orchestrate_event(event)
            encrypted_event = self.encryption_service.encrypt(
                json.dumps(orchestrated_event)
            )
            response = self.http_client.post(EncryptedEvent(**encrypted_event))
            return response.status_code
        except Exception as e:
            logger.exception("Error tracking event: %s", e)
        return None
