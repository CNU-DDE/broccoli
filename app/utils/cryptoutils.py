import hashlib
import json

def hash_dict(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf8')).hexdigest()
