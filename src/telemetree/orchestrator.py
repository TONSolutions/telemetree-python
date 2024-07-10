import re
from datetime import datetime
from telethon.utils import resolve_inline_message_id, get_peer
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import telethon


class ForwardedEventHandler:
    def __init__(self):
        self.payload = {}

    def sanitize_data(self, data):
        """Recursively sanitize data, allowing only specific characters in strings."""
        if isinstance(data, dict):
            return {k: self.sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(v) for v in data]
        elif isinstance(data, str):
            return re.sub(r"[^a-zA-Z0-9_ .,@!-]", "", data)
        else:
            return data

    def validate_data(self, data):
        """Validate essential keys in the data."""
        essential_keys = ["context", "body"]
        missing_keys = [key for key in essential_keys if key not in data]
        if missing_keys:
            raise ValueError(f"Missing essential data keys: {', '.join(missing_keys)}")

    def handle_inline_message(self, inline_message_id):
        """Extract details from inline message ID."""
        try:
            message_id, peer, dc_id, access_hash = resolve_inline_message_id(
                inline_message_id
            )
        except telethon.errors.rpcerrorlist.MessageIdInvalidError:
            return None

        return {
            "message_id": message_id,
            "peer": peer,
            "dc_id": dc_id,
            "access_hash": access_hash,
        }

    def event_handler_mapping(self):
        """Map event types to their handler functions for cleaner orchestration."""
        return {
            "chosen_inline_result": self.handle_chosen_inline_result,
            "inline_query": self.handle_inline_query,
            "my_chat_member": self.handle_chat_member_update,
            "message": self.handle_message,
        }

    def orchestrator(self, update):
        """Main function to orchestrate event handling and data processing."""
        self.collect_request_context_data()
        event_type = next(
            (
                key
                for key in self.event_handler_mapping().keys()
                if key in update and update[key] is not None
            ),
            None,
        )

        self.payload["app"] = update.get("appName", "bot")
        self.payload["eventSource"] = "python-sdk-v2"
        self.payload["isAutocapture"] = True
        self.payload["eventType"] = event_type.replace("/", "") if event_type else None

        if event_type:
            self.event_handler_mapping()[event_type](update)

        self.payload["eventparams"] = self.payload.get("eventDetails", {}).pop(
            "params", {}
        )
        self.payload["eventdetails"] = {
            "startParameter": self.payload.get("eventDetails", {}).get(
                "startParameter", "N/A"
            ),
            "path": self.payload.get("eventDetails", {}).get("path", "N/A"),
        }

        # Handle remaining parameters
        self.payload["referrerType"] = self.payload.get("referrerType", "Direct")
        self.payload["referrer"] = self.payload.get("referrer", "0")
        self.payload["sessionIdentifier"] = self.payload.get("sessionIdentifier")

        return self.payload

    def collect_request_context_data(self):
        """Collect context data from the request."""
        self.payload["timestamp"] = int(datetime.now().timestamp())

    def collect_from_info(self, from_object):
        """Collect information about the message sender."""
        try:
            user_id = from_object["entity_id"]
        except KeyError:
            user_id = from_object["id"]
        self.payload["telegramID"] = str(user_id)
        self.payload["isBot"] = from_object.get("is_bot", False)
        self.payload["language"] = from_object.get("language_code", "N/A")
        self.payload["device"] = "unknown"

        self.payload["userDetails"] = {
            "username": from_object.get("username", ""),
            "firstName": from_object.get("first_name", ""),
            "lastName": from_object.get("last_name", "") or "",
            "isPremium": from_object.get("is_premium", False),
            "writeAccess": True,
        }

    def handle_inline_query(self, body):
        """Handle inline query events."""
        inline_query = body["inline_query"]
        self.payload["eventType"] = "Inline query"
        self.payload["eventDetails"] = {
            "startParameter": inline_query["query"],
            "path": "",
        }
        self.collect_from_info(inline_query["from"])

    def handle_chosen_inline_result(self, body):
        """Handle chosen inline result events."""
        chosen_inline_result = body["chosen_inline_result"]
        self.payload["eventType"] = "Chosen inline query"
        self.payload["eventDetails"] = {
            "startParameter": chosen_inline_result["query"],
            "result": chosen_inline_result["result_id"],
            "path": "",
        }
        inline_message_id = self.handle_inline_message(
            chosen_inline_result["inline_message_id"]
        )
        if inline_message_id:
            resolved_peer = get_peer(inline_message_id["peer"])
            self.assign_chat_type_details(resolved_peer, inline_message_id)
        self.collect_from_info(chosen_inline_result["from"])

    def handle_chat_member_update(self, body):
        """Handle chat member update events with detailed status changes."""
        my_chat_member = body["my_chat_member"]
        self.payload["eventType"] = "Chat member update"

        # Extract chat information
        chat_details = {
            "chatType": my_chat_member["chat"]["type"],
            "chatId": my_chat_member["chat"]["id"],
        }

        # Determine the update type based on old and new member statuses
        old_status = my_chat_member["old_chat_member"]["status"]
        new_status = my_chat_member["new_chat_member"]["status"]

        if old_status != new_status:
            # Handle common status transitions
            if new_status == "member":
                update_type = "User joined"
            elif new_status == "left":
                update_type = "User left"
            elif new_status == "kicked":
                update_type = "User kicked/banned"
            elif new_status == "administrator":
                update_type = "User promoted to administrator"
            elif new_status == "restricted":
                update_type = "User restricted"
            else:
                update_type = "Other"
        else:
            update_type = "No change"

        # Add detailed update information
        self.payload["eventDetails"] = {
            **chat_details,
            "path": "",
            "startParameter": "",
            "updateType": update_type,
            "oldStatus": old_status,
            "newStatus": new_status,
        }

        # Collect information about the user who triggered the update
        self.collect_from_info(my_chat_member["from"])

    def handle_message(self, body):
        """Handle message events."""
        message = body["message"]
        self.payload["eventType"] = "Message"

        try:
            chatId = message["chat"]["id"]
        except KeyError:
            chatId = message["from"]["entity_id"]

        self.payload["eventDetails"] = {
            "startParameter": message.get("text", ""),
            "path": "",
            "chatType": message["chat"]["type"],
            "chatId": chatId,
            "messageId": message["message_id"],
            "text": message.get("text", ""),
            "messageLength": len(message.get("text", "")),
        }
        try:
            if "/start" in message.get("text", ""):
                self.payload["eventDetails"]["startParameter"] = message["text"].split(
                    " "
                )[1]
        except IndexError:
            self.payload["eventDetails"]["startParameter"] = ""

        self.collect_from_info(message["chat"])

    def assign_chat_type_details(self, resolved_peer, inline_message_id):
        """Assign chat type details based on the resolved peer."""
        event_details = self.payload.get("eventDetails", {})
        if isinstance(resolved_peer, PeerUser):
            event_details["chatType"] = "private"
            event_details["chat"] = resolved_peer.user_id
        elif isinstance(resolved_peer, PeerChannel):
            event_details["chatType"] = "channel"
            event_details["chat"] = (
                f"https://t.me/c/{resolved_peer.channel_id}/{inline_message_id['message_id']}"
            )
        elif isinstance(resolved_peer, PeerChat):
            event_details["chatType"] = "chat"
            event_details["chat"] = (
                f"https://t.me/c/{resolved_peer.chat_id}/{inline_message_id['message_id']}"
            )
        self.payload["eventDetails"] = event_details


def orchestrate_event(event):
    handler = ForwardedEventHandler()
    return handler.orchestrator(event)
