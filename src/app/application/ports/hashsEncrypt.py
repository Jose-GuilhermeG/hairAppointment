from abc import ABC , abstractmethod

class IHashEncrypt(ABC):
    @staticmethod
    @abstractmethod
    def encrypt(content : str)->str:
        pass

    @staticmethod
    @abstractmethod
    def verify(content : str , verify_str : str)->bool:
        pass

class IEncryptData(ABC):
    @staticmethod
    @abstractmethod
    def encrypt(content : str)->str:
        pass

    @staticmethod
    @abstractmethod
    def decode(content : str)->str:
        pass
