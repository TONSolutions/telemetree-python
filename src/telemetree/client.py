import json
from src.telemetree.config import Config
from src.telemetree.http_client import HttpClient
from src.telemetree.telemetree_schemas import EncryptedEvent
from src.telemetree.telegram_schemas import Update
from src.telemetree.encryption import EncryptionService
from src.telemetree.event_builder import EventBuilder
from src.telemetree.exceptions import CustomEventNotSupported


class TelemetreeClient:
    def __init__(self, api_key: str, project_id: str) -> None:
        self.api_key = api_key
        self.project_id = project_id

        self.settings = Config(self.api_key, self.project_id)

        self.url = self.settings.config.host
        self.auto_capture = self.settings.config.auto_capture_telegram
        self.events = self.settings.config.auto_capture_telegram_events
        self.commands = self.settings.config.auto_capture_commands
        self.public_key = self.settings.config.public_key

        self.ecnryption_service = EncryptionService(self.public_key)
        self.http_client = HttpClient(self.settings)
        self.event_builder = EventBuilder(self.settings)

    def track(self, event: dict) -> None:
        """
        Tracks a Telegram update.

        Args:
            update (dict): The Telegram update to track.
        """
        event = self.event_builder.parse_telegram_update(event)

        if event:
            encrypted_event = self.ecnryption_service.encrypt(json.dumps(event.dict()))
            self.http_client.post(EncryptedEvent(event=encrypted_event))
        else:
            raise CustomEventNotSupported("We do not support non-Telegram events yet.")
