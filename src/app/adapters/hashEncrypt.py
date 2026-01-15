import base64
import hashlib
import hmac

from bcrypt import checkpw, gensalt, hashpw

from src.app.application.ports.hashsEncrypt import IEncryptData, IHashEncrypt
from src.configs.settings import SECRET_KEY


class BcryptHashEncrypt(IHashEncrypt):

    def encrypt(self,content : str ,encode : str = "utf8", salts : bytes = gensalt())->str:
        return hashpw(content.encode(encode) , salts).decode(encode)

    def verify(self,content : str, verify_str : str , encode : str = "utf8"):
        return checkpw(content.encode(encode) , verify_str.encode(encode))

class Base64Encrypt(IEncryptData):
    def encrypt(self,content: str, encode: str = "utf-8") -> str:
        content_ecode = content.encode(encode)
        signature = hmac.new(SECRET_KEY.encode(encode), content_ecode, hashlib.sha256).digest() #type: ignore[union-attr]
        token_bytes = content_ecode + b"." + signature

        return base64.urlsafe_b64encode(token_bytes).decode(encode)

    def decode(self,content: str, encode: str = "utf-8") -> str | None:
        try:
          token_bytes = base64.urlsafe_b64decode(content.encode(encode))
          raw_uuid, signature = token_bytes.split(b".", 1)
          expected_signature = hmac.new(SECRET_KEY.encode(encode), raw_uuid, hashlib.sha256).digest() #type: ignore[union-attr]

          if hmac.compare_digest(signature, expected_signature):
              return raw_uuid.decode(encode)
          else:
              return None
        except Exception:
            return None
