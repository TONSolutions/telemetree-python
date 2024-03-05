from typing import Optional
from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    """
    Represents a base user entity.

    Attributes:
        entity_id (int): The ID of the user entity.
        first_name (str): The first name of the user.
        last_name (Optional[str]): The last name of the user (optional).
        username (Optional[str]): The username of the user (optional).
    """

    entity_id: int = Field(..., alias="id")
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class FromUser(BaseUser):
    """
    Represents a user who sent a message.

    Attributes:
        entity_id (int): The unique identifier of the user.
        is_bot (bool): Indicates whether the user is a bot or not.
        first_name (str): The first name of the user.
        last_name (Optional[str]): The last name of the user (optional).
        username (Optional[str]): The username of the user (optional).
        language_code (Optional[str]): The language code of the user (optional).
        is_premium (Optional[bool]): Indicates whether the user is a premium user or not (optional).
    """

    is_bot: bool
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None


class Chat(BaseUser):
    """
    Represents a chat entity.

    Attributes:
        entity_id (int): The ID of the chat.
        first_name (str): The first name of the chat user.
        last_name (Optional[str]): The last name of the chat user (optional).
        username (Optional[str]): The username of the chat user (optional).
        type (str): The type of the chat.
    """

    type: str


class InlineQuery(BaseModel):
    """
    Represents an inline query.

    Attributes:
        entity_id (str): The ID of the inline query.
        from_user (FromUser): The user who sent the inline query.
        query (str): The query text.
        offset (str): The offset for the results.
    """

    entity_id: str = Field(..., alias="id")
    from_user: FromUser = Field(..., alias="from")
    query: str
    offset: str


class ChosenInlineResult(BaseModel):
    """
    Represents a chosen inline result.

    Attributes:
        entity_id (str): The ID of the entity.
        from_user (FromUser): The user who sent the query.
        inline_message_id (str): The ID of the inline message.
        query (str): The query that was used to obtain the result.
        result_id (str): The ID of the chosen result.
    """

    from_user: FromUser = Field(..., alias="from")
    inline_message_id: str
    query: str
    result_id: str


class Message(BaseModel):
    """
    Represents a message entity.

    Attributes:
        entity_id (int): The ID of the message entity.
        from_user (FromUser): The user who sent the message.
        chat (Chat): The chat where the message was sent.
        date (int): The timestamp of the message.
        text (str): The content of the message.
    """

    message_id: int
    from_user: FromUser = Field(..., alias="from")
    chat: Chat
    date: int
    text: str


class EditedMessage(Message):
    edit_date: int


class ChatMember(BaseModel):
    """
    Represents a member of a chat.

    Attributes:
        user (FromUser): The user associated with the chat member.
        status (str): The status of the chat member.
    """

    user: FromUser
    status: str


class MyChatMember(BaseModel):
    """
    Represents a chat member in the MyChatMember class.

    Attributes:
        chat (Chat): The chat to which the member belongs.
        from_user (FromUser): The user who initiated the action.
        date (int): The date when the action occurred.
        old_chat_member (ChatMember): The previous chat member state.
        new_chat_member (ChatMember): The updated chat member state.
    """

    chat: Chat
    from_user: FromUser = Field(..., alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember


class Update(BaseModel):
    """
    Represents an update received from the Telegram Bot API.

    Attributes:
        update_id (int): The update's unique identifier.
        message (Optional[Message]): New incoming message of any kind — text, photo, sticker, etc.
        edited_message (Optional[Message]): New version of a message that is known to the bot and was edited.
        inline_query (Optional[InlineQuery]): New incoming inline query.
        chosen_inline_result (Optional[ChosenInlineResult]): The result of an inline query that was chosen by a user and sent to their chat partner.
        my_chat_member (Optional[MyChatMember]): A chat member's status was updated in the chat.
    """

    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[EditedMessage] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    my_chat_member: Optional[MyChatMember] = None
