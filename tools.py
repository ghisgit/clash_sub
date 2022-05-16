import config

import requests


def geturl(url):
    res = requests.get(url, headers={
        'user-agent': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'
    })
    return res.text

def readNodeconfig(n) -> dict:
    return config.sub_config.get(n)

def readTimeout() -> int:
    return config.timeout
