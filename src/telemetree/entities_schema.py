from typing import Optional
from pydantic import BaseModel


class FromUser(BaseModel):
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

    entity_id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    is_premium: Optional[bool]


class Chat(BaseModel):
    """
    Represents a chat entity.

    Attributes:
        entity_id (int): The ID of the chat.
        first_name (str): The first name of the chat user.
        last_name (Optional[str]): The last name of the chat user (optional).
        username (Optional[str]): The username of the chat user (optional).
        type (str): The type of the chat.
    """

    entity_id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
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

    entity_id: str
    from_user: FromUser
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

    entity_id: str
    from_user: FromUser
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

    entity_id: int
    from_user: FromUser
    chat: Chat
    date: int
    text: str


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
    from_user: FromUser
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
