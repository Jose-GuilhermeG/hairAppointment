from bcrypt import checkpw , gensalt , hashpw
import base64
import hmac
import hashlib

from src.app.application.ports.hashsEncrypt import IHashEncrypt , IEncryptData
from src.configs.settings import SECRET_KEY


class BcryptHashEncrypt(IHashEncrypt):

    @staticmethod
    def encrypt(content : str ,encode : str = "utf8", salts : bytes = gensalt())->str:
        return hashpw(content.encode(encode) , salts).decode(encode)

    @staticmethod
    def verify(content : str, verify_str : str , encode : str = "utf8"):
        return checkpw(content.encode(encode) , verify_str.encode(encode))

class Base64Encrypt(IEncryptData):
    @staticmethod
    def encrypt(content: str, encode: str = "utf-8") -> str:
        content_ecode = content.encode(encode)
        signature = hmac.new(SECRET_KEY.encode(encode), content_ecode, hashlib.sha256).digest()
        token_bytes = content_ecode + b"." + signature

        return base64.urlsafe_b64encode(token_bytes).decode(encode)

    @staticmethod
    def decode(content: str, encode: str = "utf-8") -> str:
        try:
          token_bytes = base64.urlsafe_b64decode(content.encode(encode))
          raw_uuid, signature = token_bytes.split(b".", 1)
          expected_signature = hmac.new(SECRET_KEY.encode(encode), raw_uuid, hashlib.sha256).digest()

          if hmac.compare_digest(signature, expected_signature):
              return raw_uuid.decode(encode)
          else:
              return None
        except Exception:
            return None
