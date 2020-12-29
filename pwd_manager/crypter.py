# ---------------------------------------------------------------------------- #
#                      Symmetric Encryption with password                      #
# ---------------------------------------------------------------------------- #
# taken from link below
# https://cryptography.io/en/latest/fernet.html#using-passwords-with-fernet
# cause you don't want to mess up cryptography yourself

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken


def encrypt(msg, pwd):
    """encrypt msg with pwd using fernet

    Args:
        msg (bytes): payload to encrypt
        pwd (bytes): password to encrypt with

    Returns:
        result (bytes): encrypted bytes (salt is prepended)
    """
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd))
    f = Fernet(key)
    res = f.encrypt(msg)
    return salt + res

def decrypt(payload, pwd):
    """decrypts a payload with password and salt

    Args:
        payload (bytes): payload to encrypt
        pwd (bytes): password to encrypt with
        salt (bytes): salt

    Returns:
        (boolean, bytes): success, decrypted payload
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=payload[:16],
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd))
    f = Fernet(key)

    try:
        result = f.decrypt(payload[16:])
        return True, result

    except InvalidToken:
        return False, None
    



