from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from requests import Response


def convert_public_key(rsa_public_key):
    # Load the RSA public key
    key = serialization.load_pem_public_key(
        rsa_public_key.encode(), backend=default_backend()
    )

    # Convert to the correct format
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem.decode()
