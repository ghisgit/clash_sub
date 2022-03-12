import re

from BaseParse import base64_decode


class SsrNode:
    def __init__(self) -> None:
        self.skip_node = ['剩余流量', '过期时间']
        self.in_node = ''
        self.ex_node = ''
        self.host_ = None
        self.udp_ = None

        self.__name = ''
        self.__server = ''
        self.__protocol = ''
        self.__method = ''
        self.__obfs = ''
        self.__password = ''
        self.__obfsparam = ''
        self.__protocolparam = ''

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, t):
        self.__name = t

    @property
    def server(self):
        return self.__server
    @server.setter
    def server(self, t):
        self.__server = t

    @property
    def protocol(self):
        return self.__protocol
    @protocol.setter
    def protocol(self, t):
        self.__protocol = t

    @property
    def method(self):
        return self.__method
    @method.setter
    def method(self, t):
        self.__method = t

    @property
    def obfs(self):
        return self.__obfs
    @obfs.setter
    def obfs(self, t):
        self.__obfs = t

    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, t):
        self.__password = t

    @property
    def obfsparam(self):
        return self.__obfsparam
    @obfsparam.setter
    def obfsparam(self, t):
        self.__obfsparam = t

    @property
    def protocolparam(self):
        return self.__protocolparam
    @protocolparam.setter
    def protocolparam(self, t):
        self.__protocolparam = t

    def loads(self, ss):
        node_urls = base64_decode(ss)
        node_url_list = [i for i in node_urls.split('\n') if i]
        node_list = []
        for v in node_url_list:
            node = self.load(v)
            if node:
                node_list.append(node)
        return node_list

    def load(self, s):
        node_url = re.match('(.*)://(.*)', s)
        if node_url[1] != 'ssr':
            return
        ssr_node = base64_decode(node_url[2])
        ssr_base = ssr_node.split('/?')
        ssr_up = ssr_base[0].split(':')
        ssr_down = ssr_base[1].split('&')

        self.server = ssr_up[0]
        self.port = ssr_up[1]
        self.protocol = ssr_up[2]
        self.method = ssr_up[3]
        self.obfs = ssr_up[4]
        self.password =base64_decode(ssr_up[5])

        for i in ssr_down:
            k = i.split('=')[0]
            try:
                v = i.split('=')[1]
            except:
                v = ''

            if k == 'protoparam':
                self.protocolparam = base64_decode(v)
            elif k == 'obfsparam':
                self.obfsparam = base64_decode(v)
            elif k == 'remarks':
                self.name = base64_decode(v)
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
            self.obfsparam = self.host_

        print(self.name)
        node = f'- name: {self.name}\n'
        node += (' '*2 + 'type: ssr\n')
        node += (' '*2 + f'server: {self.server}\n')
        node += (' '*2 + f'port: {self.port}\n')
        node += (' '*2 + f'cipher: {self.method}\n')
        node += (' '*2 + f'password: {self.password}\n')
        node += (' '*2 + f'obfs: {self.obfs}\n')
        node += (' '*2 + f'protocol: {self.protocol}')
        if self.obfsparam:
            node += ('\n' + ' '*2 + f'obfs-param: {self.obfsparam}')
        if self.protocolparam:
            node += ('\n' + ' '*2 + f'protocol-param: {self.protocolparam}')
        try:
            if int(self.udp_) > 0:
                node += ('\n' + ' '*2 + f'udp: true')
            else:
                node += ('\n' + ' '*2 + f'udp: false')
        except:
            node += ('\n' + ' '*2 + f'udp: false')
        temp_in_node = self.in_node
        temp_ex_node = self.ex_node
        temp_host = self.host_
        temp_udp = self.udp_
        self.__init__()
        self.in_node = temp_in_node
        self.ex_node = temp_ex_node
        self.host_ = temp_host
        self.udp_ = temp_udp
        return node
