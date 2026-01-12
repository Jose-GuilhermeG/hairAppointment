class ValidateException(Exception):
    def __init__(self, message : str = "Validation exception"):
        super().__init__(message)
        self.message = message

class EmpatyFieldException(ValidateException):
    def __init__(self, message = "Field can't ve null or empty"):
        super().__init__(message)

class OddFieldException(ValidateException):
    def __init__(self, message = "Field can't be odd"):
        super().__init__(message)

class InternalException(Exception):
    def __init__(self, message : str = "err internal"):
        super().__init__(message)
        self.message = message

class IntegrityException(InternalException):
    def __init__(self, message="integrity data err"):
        super().__init__(message)

class UnauthorizedException(InternalException):
    def __init__(self, message = "Unauthorized"):
        super().__init__(message)
