from rest_framework import status

class DIDReqError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)

class JWTValidationError(Exception):
    def __init__(self, message) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(message)
