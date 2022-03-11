import os
import re
import time

import requests
from flask import Flask, request
from markupsafe import escape

from node import node
from ip import domain_for_ip
from config import sub_config, timeout

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>hello</h1>'


with app.test_request_context('/proxies'):
    assert request.path == '/proxies'
@app.route('/proxies')
def proxies():
    try:
        urls = request.args.get('url').split('|')
        include = request.args.get('include')
        exclude = request.args.get('exclude')
        host = request.args.get('host')
        udp = request.args.get('udp')
        print(f'include: {include}\nexclude: {exclude}\nhost: {host}\nudp: {udp}')
        LNodes = []
        for i in urls:
            res = requests.get(i, headers={
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KH"
                + "TML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
            })
            LNodes += node(res.text, host, udp, include, exclude)
        text = 'proxies:\n'
        for i in LNodes:
            text += '\n'.join(['  '+j for j in i.split('\n')])
            text += '\n'
        return text
    except:
        return 'error'

with app.test_request_context('/getrules'):
    assert request.path == '/getrules'
@app.route('/getrules')
def getrules():
    url = request.args.get('url')
    ip_ = request.args.get('ip')
    if not ip_ :
        ip_ = 0
    res = requests.get(url)
    data = res.text
    if int(ip_):
        rules = re.findall('DOMAIN,(.*)', res.text)
        for i in rules:
            ips = domain_for_ip(i)
            for j in ips:
                data += ('\n' + ' '*2 + f'- IP-CIDR,{j}/32')
        return data
    else:
        return data

@app.route('/class/<name>/<localfile>')
def group(name, localfile):
    try:
        if not os.path.lexists('sub'):
            os.mkdir('sub')
        name = escape(name)
        localfile = escape(localfile)
        if not os.path.lexists(f'sub/{name}'):
            os.mkdir(f'sub/{name}')
        try:
            file_time = int(os.stat(f'sub/{name}/{localfile}.yaml').st_mtime)
        except:
            file_time = 0
        new_time = int(time.time())
        if (new_time - file_time) > timeout:
            sub = sub_config.get(name)
            urls = sub.get('url').split('|')
            include = sub.get('include')
            exclude = sub.get('exclude')
            host = sub.get('host')
            udp = sub.get('udp')
            group = sub.get('list')
            print(f'include: {include}\nexclude: {exclude}\nhost: {host}\nudp: {udp}')
            LNodes = []
            for i in urls:
                res = requests.get(i, headers={
                    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KH"
                    + "TML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
                })
                LNodes += node(res.text, host, udp, include, exclude)
            for k,v in group.items():
                with open(f'sub/{name}/{k}.yaml', 'w', encoding='utf8') as f:
                    f.write('proxies:\n')
                    for i in LNodes:
                        if re.search(v, i):
                            f.write('\n'.join(['  '+j for j in i.split('\n')]))
                            f.write('\n')
            f = open(f'sub/{name}/{localfile}.yaml', encoding='utf8')
            data = f.read()
            f.close()
            return data
        else:
            f = open(f'sub/{name}/{localfile}.yaml', encoding='utf8')
            data = f.read()
            f.close()
            return data
    except:
        return 'error'
