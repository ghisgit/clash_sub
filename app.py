import os
import time
import json

from flask import Flask
from markupsafe import escape

import node.parse as parse



app = Flask(__name__)



if not os.path.lexists('cache'):
    os.mkdir('cache')
if not os.path.lexists('cache/sub'):
    os.mkdir('cache/sub')



@app.route('/')
def hello():
    return '<h1>hello</h1>'

@app.route('/config/<name>/<rule>')
def config(name, rule):
    name = escape(name)
    rule = escape(rule)
    if not os.path.lexists(f'cache/sub/{name}'):
        os.mkdir(f'cache/sub/{name}')
    global_config = json.load(open('config.json')).get('global')
    config = json.load(open('config.json')).get(name)
    config['in'] = config['in'] if config['in'] else global_config['in']
    config['out'] = config['out'] if config['out'] else global_config['out']
    config['ipout'] = config['ipout'] if config['ipout'] else global_config['ipout']
    config['udp'] = config['udp'] if config['udp'] else global_config['udp']
    config['tls'] = config['tls'] if config['tls'] else global_config['tls']
    config['cert'] = config['cert'] if config['cert'] else global_config['cert']
    config['host'] = config['host'] if config['host'] else global_config['host']
    try:
        filetime = os.path.getmtime(f'cache/sub/{name}/{rule}.yaml')
    except:
        filetime = 0
    newtime = time.time()

    if int(newtime - filetime) > global_config['cache']:
        with open(f'cache/sub/{name}/servers.yaml', 'w+', encoding='utf8') as f:
            f.write('payload:')
        for k,_ in config.get('filter').items():
            with open(f'cache/sub/{name}/{k}.yaml', 'w+', encoding='utf8') as f:
                f.write('proxies:')
        parse.SubParse(name, config)
        return open(f'cache/sub/{name}/{rule}.yaml', encoding='utf8').read()
    else:
        return open(f'cache/sub/{name}/{rule}.yaml', encoding='utf8').read()



if __name__ == '__main__':
    app.run('127.0.0.1', '11180')
