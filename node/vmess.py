import re
import json

from node.BaseParse import base64_decode


class VmessNode():
    def __init__(self, link, host=None, udp=None, in_node=[], out_node=[]) -> None:
        xq = re.match (r'vmess://(.*)', link)
        if isinstance(xq, re.Match):
            xq = json.loads(base64_decode(xq.group(1)))
            self.__data = ''
            self.out_node = ['剩余流量', '过期时间'] + out_node
            self.in_node = in_node

            self.name = xq['ps']
            self.type = 'vmess'
            self.server = xq['add']
            self.port = xq['port']
            self.uuid = xq['id']
            self.alterId = xq['aid']
            self.cipher = 'auto'
            self.udp = 'true' if udp==1 else 'false'
            self.tls = 'true' if xq.get('tls') else 'false'
            self.scv = 'true' if host else 'false' if xq.get('verify_cert') else 'true'
            self.servername = host if host else self.server
            if xq['net'] =='ws':
                self.network = 'ws'
            elif xq['net'] == 'tcp' and xq['type'] == 'http':
                self.network = 'http'
            else:
                self.network = xq['net']
            self.path = '/' if not xq.get('path') else xq.get('path')
            self.host = host if host else xq['host']
        else:
            self.__data = None

    def __str__(self) -> str:
        if not isinstance(self.__data, str):
            return ''

        print(self.name)

        for inn in self.in_node:
            if not re.search(inn, self.name):
                return ''

        for outn in self.out_node:
            if re.search(outn, self.name):
                return ''

        self.__data = f'- name: \"{self.name}\"\n'
        self.__data += (' '*2 + f'type: {self.type}\n')
        self.__data += (' '*2 + f'server: {self.server}\n')
        self.__data += (' '*2 + f'port: {self.port}\n')
        self.__data += (' '*2 + f'uuid: {self.uuid}\n')
        self.__data += (' '*2 + f'alterId: {self.alterId}\n')
        self.__data += (' '*2 + f'cipher: {self.cipher}\n')
        self.__data += (' '*2 + f'udp: {self.udp}\n')
        self.__data += (' '*2 + f'tls: {self.tls}')
        if self.tls == 'true':
            self.__data += ('\n' + ' '*2 + f'skip-cert-verify: {self.scv}\n')
            self.__data += (' '*2 + f'servername: {self.servername}')
        if self.network == 'ws':
            self.__data += ('\n' + ' '*2 + f'network: {self.network}\n')
            self.__data += (' '*2 + 'ws-opts:\n')
            self.__data += (' '*4 + f'path: {self.path}\n')
            self.__data += (' '*4 + 'headers:\n')
            self.__data += (' '*6 + f'host: {self.host}')
        elif self.network == 'http':
            self.__data += ('\n' + ' '*2 + f'network: {self.network}\n')
            self.__data += (' '*2 + 'http-opts:\n')
            self.__data += (' '*4 + 'path:\n')
            self.__data += (' '*6 + f'- \"{self.path}\"\n')
            self.__data += (' '*4 + 'headers:\n')
            self.__data += (' '*6 + 'Host:\n')
            self.__data += (' '*8 + f'- {self.host}')
        else:
            self.__data += ('\n' + ' '*2 + f'network: {self.network}')
        return self.__data

    @property
    def node(self):
        return self.__str__()
