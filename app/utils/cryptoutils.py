import hashlib, json, jwt, time, ecies, base64
from django.conf import settings
from ..errors import JWTValidationError

def hash_dict(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf8')).hexdigest()

# Define JWT
# Ref: https://datatracker.ietf.org/doc/html/rfc7519#page-8
def gen_JWT(did):
    curr_time = int(time.time())

    payload = {
        'iss': settings.FE_HOST,                    # Token issuer
        'iat': curr_time,                           # Issued at
        'nbf': curr_time,                           # Not before
        'exp': curr_time + int(settings.JWT_EXPR),  # Expiration
        'sub': did                                  # Subject od the token
    }
    return jwt.encode(payload, settings.JWT_SECR, algorithm=settings.JWT_ALGO)

def verify_JWT(token):
    try:
        return jwt.decode(token, settings.JWT_SECR, algorithms=[settings.JWT_ALGO])["sub"]
    except jwt.exceptions.InvalidTokenError as err:
        raise JWTValidationError(err)

def secp256k1_encrypt(hex_pubkey, plain):
    return base64.b64encode(ecies.encrypt(hex_pubkey, plain.encode())).decode("ASCII")
