from typing import Optional
import logging

from src.telemetree.telegram_schemas import Update
from src.telemetree.config import Config

logger = logging.getLogger("telemetree.event_builder")


class EventBuilder:
    def __init__(self, settings: Config) -> None:
        self.settings = settings
        self.config = self.settings.config
        self.events_to_track = set(self.config.auto_capture_telegram_events)
        self.commands_to_track = set(self.config.auto_capture_commands)
        self.app_name = self.config.app_name

    def parse_telegram_update(self, update_dict: dict) -> Optional[Update]:
        """
        Parses a Telegram update dictionary and returns an Update object if the update should be tracked.

        Args:
            update_dict (dict): The Telegram update dictionary.

        Returns:
            Optional[Update]: The parsed Update object if the update should be tracked, None otherwise.
        """
        update = Update(**update_dict)
        update.app_name = self.app_name

        return update if self.should_track_update(update) else None

    def should_track_update(self, update: Update) -> bool:
        """
        Determines whether a given Telegram update should be tracked based on the configured events and commands.

        Args:
            update (Update): The Telegram update object.

        Returns:
            bool: True if the update should be tracked, False otherwise.
        """
        if self._is_trackable_message_event(update):
            return self._should_track_message(update)
        return self._should_track_event(update)

    def _is_trackable_message_event(self, update: Update) -> bool:
        """
        Checks if the update contains a trackable message event (new message or edited message).

        Args:
            update (Update): The Telegram update object.

        Returns:
            bool: True if the update contains a trackable message event, False otherwise.
        """
        return "message" in self.events_to_track and (
            update.message or update.edited_message
        )

    def _should_track_message(self, update: Update) -> bool:
        """
        Determines whether a message should be tracked based on the configured commands.

        Args:
            update (Update): The Telegram update object containing the message.

        Returns:
            bool: True if the message should be tracked, False otherwise.
        """
        message_text = (
            update.message.text if update.message else update.edited_message.text
        )
        return any(command in message_text for command in self.commands_to_track)

    def _should_track_event(self, update: Update) -> bool:
        """
        Determines whether a non-message event should be tracked based on the configured events.

        Args:
            update (Update): The Telegram update object.

        Returns:
            bool: True if the event should be tracked, False otherwise.
        """
        return any(
            getattr(update, event, None) is not None for event in self.events_to_track
        )
