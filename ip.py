import json

import requests


parse_url = 'https://dns.google/resolve?name={}&type=A'


def domain_for_ip(domain: str):
    res = requests.get(parse_url.format(domain),
    headers={'referer': f"https://dns.google/query?name={domain}",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KH"
    + "TML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"})
    data = json.loads(res.text)
    ips = []
    for i in data.get('Answer'):
        if i.get('type') == 1:
            ips.append(i.get('data'))
    return ips
