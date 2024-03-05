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
        # Create an Update object from the dictionary
        update = Update(**update_dict)
        if self.should_track_update(update):
            return update
        return None

    def should_track_update(self, update: Update) -> bool:
        # Directly checks if the update should be tracked based on its content
        if "message" in self.events_to_track:
            if update.message:
                return self.track_telegram_message(update.message.text)
            elif update.edited_message:
                return self.track_telegram_message(update.edited_message.text)

        return self.track_telegram_event(update)

    def track_telegram_message(self, text: str) -> bool:
        # Checks if the message text matches any of the commands to track
        return any(command in text for command in self.commands_to_track)

    def track_telegram_event(self, update: Update) -> bool:
        # Check if the type of event is in the list of events to track
        for event_attr in self.events_to_track:
            if getattr(update, event_attr, None) is not None:
                return True
        return False
