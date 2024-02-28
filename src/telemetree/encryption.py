from dotenv import load_dotenv
import os
import json
from base64 import b64encode, b64decode

import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from rsa import PrivateKey, decrypt, DecryptionError, encrypt, PublicKey

from src.telemetree import constants
from src.telemetree.telemetree_schemas import EncryptedEvent
from src.telemetree.config import Config


# Function to encrypt a message using an RSA public key
def rsa_encrypt(public_key, message):
    # Convert the public key from PEM format to an rsa.PublicKey object
    rsa_key = PublicKey.load_pkcs1_openssl_pem(public_key)
    # Encrypt the message using the public key
    encrypted_message = encrypt(message, rsa_key)
    return b64encode(encrypted_message)


# Function to generate an AES key and IV
def generate_aes_key_and_iv():
    key = get_random_bytes(16)  # AES 128-bit key
    iv = get_random_bytes(16)  # AES IV
    return key, iv


# Function to encrypt a message with AES
def encrypt_with_aes(key, iv, message):
    cipher_aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher_aes.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return b64encode(encrypted)


# Main function to encrypt the message
def encrypt_message(rsa_public_key, message):
    key, iv = generate_aes_key_and_iv()

    # Encrypt the AES key and IV using the RSA public key
    encrypted_key = rsa_encrypt(rsa_public_key, key)
    encrypted_iv = rsa_encrypt(rsa_public_key, iv)

    # Encrypt the message using AES
    encrypted_body = encrypt_with_aes(key, iv, message)

    return {
        "encryptedKey": encrypted_key.decode(),  # Convert bytes to string
        "encryptedIV": encrypted_iv.decode(),  # Convert bytes to string
        "encryptedBody": encrypted_body.decode(),  # Convert bytes to string
    }
