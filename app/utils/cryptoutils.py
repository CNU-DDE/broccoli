import hashlib
import json
import jwt
from django.conf import settings

def hash_dict(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf8')).hexdigest()

def gen_JWT(payload):
    return jwt.encode(payload, settings.JWT_SECR, algorithm="HS256")
