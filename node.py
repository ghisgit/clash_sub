import re

from vmess import VmessNode
from ssr import SsrNode
from BaseParse import base_decode

def node(sub, host, udp, include, exclude):
    node_urls = base_decode(sub)
    node_url_list = [i for i in node_urls.split('\n') if i]
    node_list = []
    vmess_node = VmessNode()
    ssr_node = SsrNode()
    if host:
        vmess_node.host_ = host
        ssr_node.host_ = host
    if udp:
        vmess_node.udp_ = udp
        ssr_node.udp_ = udp
    if include:
        vmess_node.in_node = include
        ssr_node.in_node = include
    if exclude:
        vmess_node.ex_node = exclude
        ssr_node.ex_node = exclude
    for v in node_url_list:
        print(v)
        node = ''
        node_url = re.match('(.*)://', v)
        node_type = node_url[1]
        if node_type == 'ssr':
            node = ssr_node.load(v)
        elif node_type == 'vmess':
            node = vmess_node.load(v)
        if node:
            node_list.append(node)
    return node_list
