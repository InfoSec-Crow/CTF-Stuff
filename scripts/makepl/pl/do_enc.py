import base64
import urllib.parse

def base64_encode(payload):
    return base64.b64encode(payload.encode()).decode()

def url_encode(payload):
    return urllib.parse.quote_plus(payload)

def url_encode_all(payload):
    return "".join("%{0:0>2x}".format(ord(char)) for char in payload)