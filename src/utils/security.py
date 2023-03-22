import base64
import json
import os

from cryptography.fernet import Fernet


class Security:
    # TODO: improve secure, combine encrypt+hash
    KEY = os.environ.get("ENCRYPT_KEY")
    FERNET = Fernet(KEY.encode())

    @staticmethod
    def encrypt(string: str) -> str:
        # encrypt phrase
        byte_str = string.encode()
        encrypted_message = Security.FERNET.encrypt(byte_str)

        # base64
        b64_bytes = base64.b64encode(encrypted_message)
        b64_str = b64_bytes.decode()

        return b64_str

    @staticmethod
    def decrypt(b64_str: str) -> str:
        # decode b64
        b64_bytes = b64_str.encode()
        encrypted_message = base64.b64decode(b64_bytes)

        # decrypt string
        text = Security.FERNET.decrypt(encrypted_message)
        text = text.decode()

        return text
