import re
import json

from BaseParse import base_decode

class VmessNode():
    def __init__(self):
        self.skip_node = ['剩余流量', '过期时间']
        self.in_node = ''
        self.ex_node = ''
        self.host_ = None
        self.udp_ = None

        self.__name = ''
        self.__type = ''
        self.__server = ''
        self.__port = ''
        self.__uuid = ''
        self.__alterId = ''
        self.__cipher = ''
        self.__udp = ''
        self.__tls = ''
        self.__skip_cert_verify = ''
        self.__servername = ''
        self.__network = ''
        self.__net_type = ''
        self.__path = ''
        self.__host = ''
        self.__headers= {}

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, t):
        self.__name = t

    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, t):
        self.__type = t

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, t):
        self.__port = t

    @property
    def server(self):
        return self.__server
    @server.setter
    def server(self, t):
        self.__server = t

    @property
    def uuid(self):
        return self.__uuid
    @uuid.setter
    def uuid(self, t):
        self.__uuid = t

    @property
    def alterId(self):
        return self.__alterId
    @alterId.setter
    def alterId(self, t):
        self.__alterId = int(t)

    @property
    def cipher(self):
        return self.__cipher
    @cipher.setter
    def cipher(self, t):
        self.__cipher = t

    @property
    def udp(self):
        if self.__udp:
            return 'true'
        return 'false'
    @udp.setter
    def udp(self, t):
        self.__udp = t

    @property
    def tls(self):
        return self.__tls
    @tls.setter
    def tls(self, t):
        self.__tls = t

    @property
    def skip_cert_verify(self):
        return self.__skip_cert_verify
    @skip_cert_verify.setter
    def skip_cert_verify(self, t):
        self.__skip_cert_verify = t

    @property
    def servername(self):
        return self.__servername
    @servername.setter
    def servername(self, t):
        self.__servername = t

    @property
    def network(self):
        return self.__network
    @network.setter
    def network(self, t):
        self.__network = t

    @property
    def nettype(self):
        return self.__net_type
    @nettype.setter
    def nettype(self, t):
        self.__net_type = t

    @property
    def path(self):
        if self.__path:
            return self.__path
        return '/'
    @path.setter
    def path(self, t):
        self.__path = t

    @property
    def host(self):
        return self.__host
    @host.setter
    def host(self, t):
        self.__host = t

    @property
    def headers(self):
        return self.__headers
    @headers.setter
    def headers(self, t):
        self.__headers = t

    def loads(self, vs):
        node_urls = base_decode(vs)
        node_url_list = [i for i in node_urls.split('\n') if i]
        node_list = []
        for v in node_url_list:
            node = self.load(v)
            if node:
                node_list.append(node)
        return node_list

    def load(self, v):
        node_url = re.match('(.*)://(.*)', v)
        if node_url[1] != 'vmess':
            return
        v2_node = json.loads(base_decode(node_url[2]))
        # print(v2_node)
        self.name = v2_node.get('ps')
        self.type = 'vmess'
        self.server = v2_node.get('add')
        self.port = v2_node.get('port')
        self.uuid = v2_node.get('id')
        self.alterId = v2_node.get('aid')
        self.cipher = 'auto'
        self.udp = v2_node.get('udp')
        self.tls = 'true' if v2_node.get('tls') else 'false'
        self.skip_cert_verify = 'false' if v2_node.get('verify_cert') else 'true'
        self.servername = v2_node.get('sni')
        self.network = v2_node.get('net')
        self.nettype =  v2_node.get('type')
        self.path =  v2_node.get('path')
        self.host =  v2_node.get('host')
        for i in v2_node.keys():
            if re.match('header', i):
                self.__headers.update({i[6:].capitalize(): v2_node.get(f'{i}')})
        return self.generate()

    def generate(self):
        if self.skip_node:
            for i in self.skip_node:
                if re.search(i, self.name):
                    return
        if self.ex_node:
            if re.search(self.ex_node, self.name):
                return
        if self.in_node:
            if not re.search(self.in_node, self.name):
                return
        if self.host_:
            self.host = self.host_
            if self.servername:
                self.servername = self.host
            self.headers.update({'Host': self.host})
        if self.udp_:
            try:
                if int(self.udp_) > 0:
                    self.udp = 1
                else:
                    self.udp = 0
            except:
                ...

        print(self.name)
        node = f'- name: {self.name}\n'
        node += (' '*2 + f'type: {self.type}\n')
        node += (' '*2 + f'server: {self.server}\n')
        node += (' '*2 + f'port: {self.port}\n')
        node += (' '*2 + f'uuid: {self.uuid}\n')

        if isinstance(self.alterId, int):
            node += (' '*2 + f'alterId: {self.alterId}\n')
        node += (' '*2 + f'cipher: {self.cipher}\n')
        node += (' '*2 + f'udp: {self.udp}\n')
        node += (' '*2 + f'tls: {self.tls}\n')
        node += (' '*2 + f'skip-cert-verify: {self.skip_cert_verify}\n')
        if self.servername:
            node += (' '*2 + f'servername: {self.servername}\n')

        if self.network == 'ws':
            node += (' '*2 + f'network: ws\n')
            node += (' '*2 + f'ws-opts:\n')
            node += (' '*4 + f'path: {self.path}')
            if self.host:
                node += ('\n' + ' '*4 + 'headers:\n')
                node += (' '*6 + f'Host: {self.host}')

        elif self.network == 'tcp':
            if self.nettype == 'http':
                node += (' '*2 + f'network: http\n')
                node += (' '*2 + 'http-opts:\n')
                node += (' '*4 + 'path:\n')
                node += (' '*6 + f'- {self.path}')
                if self.headers:
                    node += ('\n' + ' '*4 + 'headers:')
                    for k, v in self.headers.items():
                        node += ('\n' + ' '*6 + k + ':\n')
                        node += (' '*8 + '- ' + v)

        temp_in_node = self.in_node
        temp_host = self.host_
        temp_udp = self.udp_
        self.__init__()
        self.in_node = temp_in_node
        self.host_ = temp_host
        self.udp_ = temp_udp
        return node
