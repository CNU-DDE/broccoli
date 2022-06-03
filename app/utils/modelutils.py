from ..models import User
from ..errors import AuthorizationFailedError

def is_employee(did):
    if not User.objects.filter(did = did):
        raise AuthorizationFailedError()
    return int(User.objects.get(did = did).user_type) % 2 == 1
