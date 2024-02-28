from typing import List
from pydantic import BaseModel


class BotTrackingConfig(BaseModel):
    """
    Configuration class for bot tracking.
    """

    auto_capture_telegram: bool
    public_key: str
    host: str

    auto_capture_telegram_events: List[str]
    auto_capture_commands: List[str]


class EncryptedEvent(BaseModel):
    """
    Class for encrypted events.
    """

    key: str
    iv: str
    body: str
