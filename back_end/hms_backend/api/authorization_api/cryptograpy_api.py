import hashlib
from cryptography.fernet import Fernet
from hms_backend.project_constants import constants
from flask import current_app as app


# key for encoding and decoding data-field is fixed.
# key itself is encoded to bytes & passed to Fernet object.
def encode(data):
    """
        API to do field level encryption of the database.

        Args:
            data (str): Data to encrypt

        Return:
            Encrypted Data
    """
    fernet = Fernet(app.config[constants.FERNET_KEY])
    return fernet.encrypt(data.encode())


def decode(encrypted_data):
    """
        API to do field level decryption of the database.

        Args:
            encrypted_data (str): Data to decrypt

        Return:
            Decrypted Data
    """
    fernet = Fernet(app.config[constants.FERNET_KEY])
    return fernet.decrypt(encrypted_data).decode()


def hash_encode(data):
    """
        API to do one way encryption of the data. Note this data cannot be decrypted.

        Args:
            data (str): Data to encrypt

        Return:
            Encrypted Data
    """
    return hashlib.md5(data.encode()).hexdigest()
