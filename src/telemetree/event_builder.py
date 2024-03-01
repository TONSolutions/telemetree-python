from typing import Optional
from src.telemetree.telegram_schemas import Update
from src.telemetree.config import Config


class EventBuilder:
    def __init__(self, settings: Config) -> None:
        self.settings = settings
        self.config = self.settings.config
        self.events_to_track = self.config.auto_capture_telegram_events
        self.commands_to_track = self.config.auto_capture_commands

    def parse_telegram_update(self, update_dict: dict) -> Optional[Update]:
        update = Update(**update_dict)  # Convert dict to Update object
        if self.should_track_update(update):
            return update
        return None

    def should_track_update(self, update: Update) -> bool:
        # Directly checks if the update should be tracked based on its content
        if update.message and self.track_telegram_message(update):
            return True
        return self.track_telegram_event(update)

    def track_telegram_message(self, update: Update) -> bool:
        # Checks if the message text matches any of the commands to track
        if update.message.text:
            return any(
                command in update.message.text for command in self.commands_to_track
            )
        return False

    def track_telegram_event(self, update: Update) -> bool:
        # Check if the type of event is in the list of events to track
        for event_attr in self.events_to_track:
            if getattr(update, event_attr, None) is not None:
                return True
        return False
