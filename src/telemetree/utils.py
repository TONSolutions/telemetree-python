from uuid import UUID


def validate_uuid(uuid_str: str) -> str:
    try:
        UUID(uuid_str)
        return uuid_str
    except ValueError:
        raise ValueError("Invalid key format.")
