
from flask import request

def _bearer_token(self, headers):
    if 'Authorization' in headers:
        auth = headers['Authorization'].split(' ')
        if auth[0].lower() == 'bearer':
            return auth[1]
    return None

def get_request_token():
    request.headers