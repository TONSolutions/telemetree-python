from base64 import b64encode
import logging

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from rsa import PublicKey, encrypt

from telemetree.schemas import EncryptedEvent

logger = logging.getLogger("telemetree.encryption")


class EncryptionService:
    def __init__(self, public_key):
        self.rsa_public_key = public_key

    def rsa_encrypt(self, message: bytes) -> bytes:
        """
        Encrypts a message using RSA encryption with the provided public key.

        Args:
            message (bytes): The message to encrypt.

        Returns:
            bytes: The encrypted message in base64 encoding.
        """
        try:
            # Convert bytes to hex string first, matching Go implementation
            hex_str = message.hex().encode("utf-8")

            rsa_key = PublicKey.load_pkcs1(self.rsa_public_key)
            encrypted_message = encrypt(hex_str, rsa_key)
            return b64encode(encrypted_message)
        except Exception as e:
            logger.exception("Failed to encrypt message with RSA: %s", e)
            raise ValueError(f"Failed to encrypt message with RSA: {e}") from e

    def generate_aes_key_and_iv(self) -> tuple:
        """
        Generates a random AES key and initialization vector (IV).

        Returns:
            tuple: A tuple containing the AES key and IV, both as bytes.
        """
        key = get_random_bytes(16)  # AES 128-bit key
        iv = get_random_bytes(16)  # AES IV
        return key, iv

    def encrypt_with_aes(self, key: bytes, iv: bytes, message: str) -> bytes:
        """
        Encrypts a message using AES encryption with the provided key and IV.

        Args:
            key (bytes): The AES key.
            iv (bytes): The AES initialization vector.
            message (str): The message to encrypt.

        Returns:
            bytes: The encrypted message in base64 encoding.

        Raises:
            ValueError: If the provided message is not a string.
        """
        if not isinstance(message, str):
            logger.error("Message must be a string")
            raise ValueError("Message must be a string")

        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher_aes.encrypt(pad(message.encode("utf-8"), AES.block_size))
        return b64encode(encrypted)

    def encrypt(self, message: str) -> dict:
        """
        Encrypts a message using a hybrid approach with RSA and AES encryption.

        Args:
            message (str): The message to encrypt.

        Returns:
            dict: A dictionary containing the encrypted key, IV, and message body, all base64 encoded.

        Raises:
            ValueError: If the provided message is not a string, or if an encryption error occurs.
        """
        if not isinstance(message, str):
            logger.error("Message must be a string")
            raise ValueError("Message must be a string")

        try:
            key, iv = self.generate_aes_key_and_iv()

            encrypted_key = self.rsa_encrypt(key)
            encrypted_iv = self.rsa_encrypt(iv)

            encrypted_body = self.encrypt_with_aes(key, iv, message)

            return {
                "key": encrypted_key,
                "iv": encrypted_iv,
                "body": encrypted_body,
            }
        except Exception as e:
            logger.exception("Failed to encrypt message: %s", e)
            raise ValueError(f"Failed to encrypt message: {e}") from e
