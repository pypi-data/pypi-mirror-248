import json
from urllib.parse import urlencode, quote


def object_to_query_string(params):
    encode_params = {}
    params = dict(sorted(params.items()))

    def _encode_params(params, p_key=None):
        if isinstance(params, dict):
            for key, value in params.items():
                encode_key = f"{p_key}[{key}]" if p_key else key
                _encode_params(value, encode_key)
        elif isinstance(params, (list, tuple)):
            for offset, value in enumerate(params):
                encode_key = f"{p_key}[{offset}]"
                _encode_params(value, encode_key)
        else:
            encode_params[p_key] = params

    if isinstance(params, dict):
        for key, value in params.items():
            _encode_params(value, key)

    return urlencode(encode_params, quote_via=quote)


def convert_bytes_to_str(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, list):
        return [convert_bytes_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_bytes_to_str(value) for key, value in obj.items()}
    else:
        return obj


def object_to_json(obj):
    return convert_bytes_to_str(obj)
