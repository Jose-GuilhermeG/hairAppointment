from abc import ABC, abstractmethod


class IHashEncrypt(ABC):
    @abstractmethod
    def encrypt(self,content : str)->str:
        pass

    @abstractmethod
    def verify(self,content : str , verify_str : str)->bool:
        pass

class IEncryptData(ABC):
    @abstractmethod
    def encrypt(self,content : str)->str:
        pass

    @abstractmethod
    def decode(self,content : str)->str | None:
        pass
