from pydantic import BaseModel, HttpUrl


class Config(BaseModel):
    """
    Configuration class for bot tracking.

    Attributes:
        events_host (HttpUrl): The host URL for the Telemetree service.
        tasks_host (HttpUrl): The host URL for the Telemetree service.
        public_key (str): The public key used for encryption.
        token (str): The token used for authentication.
        exp_time (int): The expiration time of the token.
    """

    events_host: HttpUrl
    tasks_host: HttpUrl
    public_key: str
    token: str
    exp_time: int


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


class Payload(BaseModel):
    """
    Class representing a payload.

    Attributes:
        update (Update): The update to be tracked.
    """

    # to implement
    pass
