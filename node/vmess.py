import re
import json

from urllib.parse import unquote

from node.tools import Base64Decode

class Vmess():
    def __init__(self, link, udp, tls, cert, host):
        self.link = link
        self.__udp = udp
        self.__tls = tls
        self.__cert = cert
        self.__host = host

    @property
    def udp(self):
        if self.__udp == 1:
            return 'true'
        elif self.__udp == -1:
            return 'false'

    @udp.setter
    def udp(self, value):
        if self.__udp == 0:
            self.__udp = 1 if value else -1

    @property
    def tls(self):
        if self.__tls == 1:
            return 'true'
        elif self.__tls == -1:
            return 'false'

    @tls.setter
    def tls(self, value):
        if self.__tls == 0:
            self.__tls = 1 if value else -1

    @property
    def cert(self):
        if self.__cert == 1:
            return 'true'
        elif self.__cert == -1:
            return 'false'

    @cert.setter
    def cert(self, value):
        if self.__cert == 0:
            self.__cert = -1 if value else 1

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = self.__host if self.__host else value

    def parse(self):
        if 'remarks' in self.link:
            test = self.link.split('?')
            test0 = re.match('^(.*?):(.*?)@(.*?):(.*?)$', Base64Decode(test[0]))
            self.cipher = test0.group(1)
            self.uuid = test0.group(2)
            self.server = test0.group(3)
            self.port = test0.group(4)

            test1 = test[1]
            t = re.search(r'remarks=(.*?)(&|$)', test1)
            self.name = f'{self.server}:{self.port}' if not isinstance(t, re.Match) else unquote(t.group(1))
            t = re.search(r'obfsParam=(.*?)(&|$)', test1)
            self.host = None if not isinstance(t, re.Match) else t.group(1)
            t = re.search(r'path=(.*?)(&|$)', test1)
            self.path = '/' if not isinstance(t, re.Match) else t.group(1)
            t = re.search(r'obfs=(.*?)(&|$)', test1)
            self.network = 'ws' if isinstance(t, re.Match) and t.group(1) == 'websocket' else None
            t = re.search(r'alterId=(.*?)(&|$)', test1)
            self.alterId = '0' if not isinstance(t, re.Match) else t.group(1)

            self.udp = None
            self.tls = None
            self.cert = None
        else:
            node = json.loads(Base64Decode(self.link))
            self.name = node['ps']
            self.server = node['add']
            self.port = node['port']
            self.uuid = node['id']
            self.alterId = node['aid']
            self.cipher = 'auto'
            self.udp = node.get('udp')
            self.tls = node.get('tls')
            self.cert = node.get('verify_cert')
            if node['net'] =='ws':
                    self.network = 'ws'
            elif node['net'] == 'tcp' and node['type'] == 'http':
                self.network = 'http'
            else:
                self.network = node['net']
            self.path = node.get('path') if node.get('path') else '/'
            self.host = node.get('host')
        return self.code()

    def code(self):
        text1 = f'- name: "{self.name}"\n' +\
        ' '*2 + 'type: vmess\n' +\
        ' '*2 + f'server: {self.server}\n' +\
        ' '*2 + f'port: {self.port}\n' +\
        ' '*2 + f'uuid: {self.uuid}\n' +\
        ' '*2 + f'alterId: {self.alterId}\n' +\
        ' '*2 + f'cipher: {self.cipher}\n' +\
        ' '*2 + f'udp: {self.udp}\n' +\
        ' '*2 + f'tls: {self.tls}\n' +\
        ' '*2 + f'skip-cert-verify: {self.cert}'
        if self.network == 'ws':
            text1 += '\n' + ' '*2 + f'network: {self.network}\n' +\
            ' ' * 2 + f'ws-opts:\n' +\
            ' ' * 4 + f'path: {self.path}'
            if self.host:
                text1 += '\n' + ' ' * 4 + 'headers:\n' +\
                ' ' * 6 + f'Host: {self.host}'
        elif self.network == 'http':
            text1 += '\n' + ' '*2 + f'network: {self.network}\n' +\
            ' ' * 2 + f'http-opts:\n' +\
            ' ' * 4 + 'path:\n' +\
            ' ' * 6 + f'- \'{self.path}\''
            if self.host:
                text1 += '\n' + ' ' * 4 + 'headers:\n' +\
                ' ' * 6 + 'Host:\n'
                ' ' * 8 + f'- {self.host}'
        return text1
