import base64

import requests


def GetResponseText(url) -> str:
    res = requests.get(url, headers={
        'user-agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'
    })
    return res.text

def Base64Decode(s:str or bytes) -> str:
    SourcerStrReplace = {b'_': b'/', b'-': b'+'}
    if isinstance(s, str):
        s = s.encode('utf8')
    for k,v in SourcerStrReplace.items():
        s = s.replace(k, v)
    b = base64.b64decode(s+b'===')
    return b.decode('utf8')
