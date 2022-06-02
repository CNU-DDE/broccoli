import requests
import json
from django.conf import settings
from ..errors import DIDReqError

def did_get_req(path, req_param=None):
    res = requests.get("http://" + settings.DID_HOST + path, params=req_param)
    body = json.loads(res.text)
    if res.status_code >= 400 or body['error'] is not None:
        raise DIDReqError(res.status_code, body['error'])
    return body['content']
