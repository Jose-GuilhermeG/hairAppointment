import pytest

from src.app.adapters.hashEncrypt import BcryptHashEncrypt
from src.app.application.ports.hashsEncrypt import IEncryptData


def get_hash_encypt()->IEncryptData:
    return BcryptHashEncrypt()

@pytest.fixture
def hash_encrypt():
    return get_hash_encypt()
