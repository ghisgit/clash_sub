import os
import re
import time

from flask import Flask, request
from markupsafe import escape

import tools
from node import vmess, ssr, trojan
from node.BaseParse import base64_decode

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>hello</h1>'

@app.route('/config/<name>/<rule>')
def config(name, rule):
    name = escape(name)
    rule = escape(rule)
    if not os.path.lexists('sub'):
        os.mkdir('sub')
    if not os.path.lexists(f'sub/{name}'):
        os.mkdir(f'sub/{name}')
    NC = tools.readNodeconfig(name) # Node Config
    if not NC:
        return 'Node config error'
    TO = tools.readTimeout() # File Timeout
    try:
        filetime = os.path.getmtime(f'sub/{name}/{rule}.yaml')
    except:
        filetime = 0
    newtime = time.time()
    if int(newtime - filetime) > TO:
        url = NC['url']
        i = NC['in']
        o = NC['out']
        h = NC['host']
        u = NC['udp']
        l = dict(NC['list'])
        for i in url.split('|'):
            try:
                basetext = tools.geturl(i)
            except:
                continue
            nodeurls = base64_decode(basetext).split('\n')
            clashNodes = []
            serverDomain = []
            for nurl in nodeurls:
                try:
                    if re.match('ssr://', nurl):
                        clashNodes.append(ssr.SsrNode(nurl, h, u, i, o).node)
                    elif re.match('trojan://', nurl):
                        clashNodes.append(trojan.TrojanNode(nurl, h, u, i, o).node)
                    elif re.match('vmess://', nurl):
                        clashNodes.append(vmess.VmessNode(nurl, h, u, i, o).node)
                except:
                    continue
        for k, v in l.items():
            with open(f'sub/{name}/{k}.yaml', 'w', encoding='utf8') as f:
                f.write('proxies:\n')
                for i in [i for i in clashNodes if i]:
                    serverDomain.append(re.search(r'server: (.*)', i).group(1))
                    if re.search(v, i):
                        f.write('\n'.join([' ' * 2 + j for j in i.split('\n')])+'\n')
        temp = []
        [temp.append(i) for i in serverDomain if not i in temp]
        with open(f'sub/{name}/servers.yaml', 'w', encoding='utf8') as f:
            f.write('payload:\n')
            for i in temp:
                if not re.match('\d+.\d+.\d+.\d+', i):
                    f.write('  - DOMAIN,' + i + '\n')
                else:
                    f.write('  - IP-CIDR,' + i + '/32\n')
    with open(f'sub/{name}/{rule}.yaml', encoding='utf8') as f:
        data = f.read()
    return data

@app.route('/getrules')
def getrules():
    url = request.args.get('url')
    return tools.geturl(url)
