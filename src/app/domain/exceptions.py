# Validation exceptions
class ValidateException(Exception):
    def __init__(self, message : str = "Validation exception"):
        super().__init__(message)
        self.message = message

class EmptyFieldException(ValidateException):
    def __init__(self, message = "Field can't ve null or empty"):
        super().__init__(message)

class OddFieldException(ValidateException):
    def __init__(self, message = "Field can't be a odd number"):
        super().__init__(message)

class EmailFieldException(ValidateException):
    def __init__(self, message = "Incorrect email"):
        super().__init__(message)

class MinLenghtFieldException(ValidateException):
    def __init__(self, message = "Validation exception"):
        super().__init__(message)

#  Internal exceptions

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
