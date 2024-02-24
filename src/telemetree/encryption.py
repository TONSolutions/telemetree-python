import json
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Util.Padding import pad
from telemetree import constants


class EncryptionService:
    def rsa_encrypt(self, public_key_str, message):
        # Import the public key
        public_key = RSA.import_key(public_key_str)
        # Initialize RSA cipher
        cipher_rsa = PKCS1_OAEP.new(public_key)
        # Encrypt and return base64 encoded message
        return b64encode(cipher_rsa.encrypt(message))

    # Function to generate a random AES key and IV
    def generate_aes_key_iv(self):
        # Generate 16 byte key and IV for AES encryption
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        return key, iv

    # Function to encrypt data using AES
    def aes_encrypt(self, key, iv, message):
        # Initialize AES cipher in CBC mode
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        # Encrypt and return base64 encoded message
        return b64encode(cipher_aes.encrypt(pad(message.encode(), AES.block_size)))

    # Main function to process and send an event
    def process_event(self, event, public_key, api_gateway, api_key):
        try:
            # Generate AES key and IV
            key, iv = self.generate_aes_key_iv()
            # Encrypt AES key and IV using RSA
            encrypted_key = self.rsa_encrypt(public_key, key)
            encrypted_iv = self.rsa_encrypt(public_key, iv)
            # Encrypt event data using AES
            encrypted_body = self.aes_encrypt(key, iv, json.dumps(event))

            # Prepare the payload with encrypted data
            payload = json.dumps(
                {
                    "key": encrypted_key.decode(),
                    "iv": encrypted_iv.decode(),
                    "body": encrypted_body.decode(),
                }
            )

            # Send a POST request with the encrypted payload
            response = requests.post(
                api_gateway,
                data=payload,
                headers={"Content-Type": "application/json", "X-Api-Key": api_key},
                timeout=constants.HTTP_TIMEOUT,
            )
            return response
        except Exception as e:
            # Print any exceptions that occur
            print(f"An error occurred: {e}")
