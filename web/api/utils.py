import json
from flask import make_response, request

JSON_MIME_TYPE = 'application/json'

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE
    return make_response(data, status, headers)

import re

def validate_fields(request, fields):
    errors = []
    data = None
    if request.content_type != JSON_MIME_TYPE:
        errors.append('Invalid Content Type')

    if request.method == 'POST':
        data = request.json
        for f in fields:
            try:
                if not data.get(f):
                    errors.append('Missing field/s (%s)' %f)
            except AttributeError:
                errors.append('Expected field/s not found(%s)' %f)
    else:
        data = request.get_json(silent=True) or {}
        for f in fields:
            data[f] = request.args.get(f)

    if errors:
        response = {"result": {}
                    ,"code": 1
                    ,"errors": errors}
        return False, response , None
    else:
        response = {"result": {}
                    ,"code": 0
                    ,"errors": []}
        return True, response, data