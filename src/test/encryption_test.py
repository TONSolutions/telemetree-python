import pytest
from Crypto.PublicKey import RSA
from rsa import PrivateKey, decrypt
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from src.telemetree.encryption import EncryptionService


# Generate or load a test RSA key for testing purposes
test_rsa_key = RSA.generate(2048)
pub_key = test_rsa_key.publickey().export_key()
private_key = test_rsa_key.export_key()


def load_private_key(private_key_data: str) -> PrivateKey:
    try:
        return PrivateKey.load_pkcs1(private_key_data)
    except ValueError as e:
        raise ValueError("Invalid private key format.") from e


def decrypt_message(encrypted_data: dict, private_key_data: str) -> str:
    """
    Decrypts the given message using the provided private key data.

    Args:
        encrypted_data (dict): A dictionary with 'key', 'iv', and 'body' keys containing the encrypted data.
        private_key_data (str): A string containing the PEM-formatted private key data.

    Returns:
        str: The decrypted message.

    Raises:
        ValueError: If decryption fails.
    """
    encrypted_key = b64decode(encrypted_data["key"])
    encrypted_iv = b64decode(encrypted_data["iv"])
    encrypted_body = b64decode(encrypted_data["body"])

    private_key = load_private_key(private_key_data)

    try:
        # Decrypt the AES key and IV with the RSA private key
        key = decrypt(encrypted_key, private_key)
        iv = decrypt(encrypted_iv, private_key)

        # Decrypt the message with the AES key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_body), AES.block_size)
        return decrypted_data.decode("utf-8")
    except Exception as e:
        raise ValueError("Decryption failed.") from e


@pytest.fixture
def encryption_service():
    return EncryptionService(pub_key)


def test_rsa_encrypt_with_valid_message(encryption_service):
    message = "Test message"
    encrypted_message = encryption_service.rsa_encrypt(message)
    assert isinstance(encrypted_message, bytes)


def test_rsa_encrypt_with_empty_message(encryption_service):
    message = ""
    encrypted_message = encryption_service.rsa_encrypt(message)
    assert isinstance(encrypted_message, bytes)


def test_rsa_encrypt_raises_error_with_invalid_key(encryption_service):
    encryption_service.rsa_public_key = b"invalid_key"
    with pytest.raises(ValueError):  # An exception should be raised for invalid RSA key
        encryption_service.rsa_encrypt("Test message")


def test_rsa_encrypt_with_large_message(encryption_service):
    # RSA encryption cannot handle large messages, so we test the limit.
    max_rsa_message_size = (
        245  # This is an approximate size for a 2048-bit key with padding.
    )
    message = "a" * max_rsa_message_size
    encrypted_message = encryption_service.rsa_encrypt(message)
    assert isinstance(encrypted_message, bytes)


def test_generate_aes_key_and_iv(encryption_service):
    key, iv = encryption_service.generate_aes_key_and_iv()
    assert isinstance(key, bytes) and len(key) == 16  # AES 128-bit key
    assert isinstance(iv, bytes) and len(iv) == 16  # AES IV


def test_generate_aes_key_and_iv_uniqueness(encryption_service):
    keys_and_ivs = {encryption_service.generate_aes_key_and_iv() for _ in range(10)}
    assert len(keys_and_ivs) == 10  # Each key and IV pair should be unique


def test_encrypt_with_aes_with_valid_inputs(encryption_service):
    key, iv = encryption_service.generate_aes_key_and_iv()
    message = "Test AES message"
    encrypted_message = encryption_service.encrypt_with_aes(key, iv, message)
    assert isinstance(encrypted_message, bytes)


def test_encrypt_with_aes_with_empty_message(encryption_service):
    key, iv = encryption_service.generate_aes_key_and_iv()
    message = ""
    encrypted_message = encryption_service.encrypt_with_aes(key, iv, message)
    assert isinstance(encrypted_message, bytes)


def test_encrypt_with_aes_non_ascii(encryption_service):
    key, iv = encryption_service.generate_aes_key_and_iv()
    message = "Test message with non-ASCII 👾🔥"
    encrypted_message = encryption_service.encrypt_with_aes(key, iv, message)
    assert isinstance(encrypted_message, bytes)


def test_encrypt_with_aes_invalid_key(encryption_service):
    key = b"invalid_key_length"
    iv = b"invalid_iv_length"
    message = "Test message"
    with pytest.raises(
        ValueError
    ):  # An exception should be raised for invalid key length
        encryption_service.encrypt_with_aes(key, iv, message)


def test_encrypt_with_valid_message(encryption_service):
    message = "Test integration message"
    encrypted_data = encryption_service.encrypt(message)
    assert isinstance(encrypted_data, dict)
    assert (
        "key" in encrypted_data and "iv" in encrypted_data and "body" in encrypted_data
    )


def test_full_encryption_and_decryption(encryption_service):
    original_message = "Full encryption and decryption test"
    encrypted_data = encryption_service.encrypt(original_message)

    decrypted_message = decrypt_message(encrypted_data, private_key)

    assert decrypted_message == original_message
