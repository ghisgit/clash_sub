import requests
from flask import Flask, request

from node import node

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
    res = requests.get(url)
    return res.text
