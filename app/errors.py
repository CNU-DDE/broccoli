from rest_framework import status
from rest_framework.response import Response
from .utils.convutils import error_message

class BaseError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = str(message)
        super().__init__(message)
    def gen_response(self):
        return Response({ "error": self.message }, status=self.status_code)

class DIDReqError(BaseError):
    def __init__(self, status_code, message):
        super().__init__(status_code, message)

class JWTValidationError(BaseError):
    def __init__(self, err):
        super().__init__(status.HTTP_401_UNAUTHORIZED, error_message(err))

class PermissionDeniedError(BaseError):
    def __init__(self, message="Permission denied"):
        super().__init__(status.HTTP_403_FORBIDDEN, message)

class AuthorizationFailedError(BaseError):
    def __init__(self, message="Authorization failed"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)

class ClientFaultError(BaseError):
    def __init__(self, message):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

class UnhandledError(BaseError):
    def __init__(self, err):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, error_message(err))
