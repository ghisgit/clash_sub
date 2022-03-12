import base64

def base64_decode(s:str or bytes):
    if isinstance(s, str):
        s = s.encode('utf8')
    kv = {b'_': b'/', b'-': b'+'}
    for k,v in kv.items():
        s = s.replace(k, v)
    b = base64.b64decode(s+b'===')
    return b.decode('utf8')
