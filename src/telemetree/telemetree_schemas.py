from typing import List
from pydantic import BaseModel


class BotTrackingConfig(BaseModel):
    """
    Configuration class for bot tracking.

    Attributes:
        auto_capture_telegram (bool): Indicates whether to automatically capture Telegram events.
        public_key (str): The public key used for encryption.
        host (str): The host URL for the Telemetree service.
        auto_capture_telegram_events (List[str]): The list of Telegram events to automatically capture.
        auto_capture_commands (List[str]): The list of commands to automatically capture.
    """

    auto_capture_telegram: bool
    public_key: str
    host: str

    auto_capture_telegram_events: List[str]
    auto_capture_commands: List[str]


class EncryptedEvent(BaseModel):
    """
    Class representing an encrypted event.

    Attributes:
        key (str): The encrypted key used for decryption.
        iv (str): The encrypted initialization vector used for decryption.
        body (str): The encrypted event data.
    """

    key: str
    iv: str
    body: str
