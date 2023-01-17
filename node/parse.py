import re

from node.vmess import Vmess
from node.ssr import Ssr
from node.trojan import Trojan

from node.tools import GetResponseText, Base64Decode



def SubParse(name, Dp: dict):
    temp = []
    for u in Dp.get('url'):
        try:
            SubBase64Text = GetResponseText(u)
        except:
            continue
        if SubBase64Text:
            NodeLinks = Base64Decode(SubBase64Text).replace('\r', '').split('\n')
            for node_link in NodeLinks:
                test = node_link.split('://')
                if test[0] == 'vmess':
                    n = Vmess(test[1], Dp.get('udp'), Dp.get('tls'), Dp.get('cert'), Dp.get('host'))
                elif test[0] == 'ssr':
                    n = Ssr(test[1], Dp.get('udp'), Dp.get('host'))
                elif test[0] == 'trojan':
                    n = Trojan(test[1], Dp.get('udp'), Dp.get('cert'), Dp.get('host'))
                else:
                    continue
                node = n.parse()
                if not node:
                    continue
                if Dp.get('in'):
                    if not re.search(Dp.get('in'), n.name, re.I):
                        continue
                if Dp.get('out'):
                    if re.search(Dp.get('out'), n.name, re.I):
                        continue
                if Dp.get('ipout'):
                    if re.search(Dp.get('ipout'), n.server, re.I):
                        continue
                if not n.server in temp:
                    with open(f'cache/sub/{name}/servers.yaml', 'a+', encoding='utf8') as f:
                        if re.match('\d+.\d+.\d+.\d+', n.server):
                            f.write('\n  - IP-CIDR,' + n.server + '/32')
                        else:
                            f.write('\n  - DOMAIN,' + n.server)
                        temp.append(n.server)
                for k,v in Dp.get('filter').items():
                    print(n.name)
                    if re.match(v, n.name):
                        with open(f'cache/sub/{name}/{k}.yaml', 'a+', encoding='utf8') as f:
                            node = '\n' + re.sub('^', ' '*2, node, flags=re.M)
                            f.write(node)
