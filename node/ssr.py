import re

from node.tools import Base64Decode

class Ssr():
    def __init__(self, link, udp, host):
        self.link = link
        self.__udp = udp
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
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = self.__host if self.__host else value


    def parse(self):
        node = re.match(r'(.*?):(.*?):(.*?):(.*?):(.*?):(.*?)/\?(.*)', Base64Decode(self.link))
        self.server = node.group(1)
        self.port = node.group(2)
        self.cipher = node.group(4)
        self.password = Base64Decode(node.group(6))
        self.obfs = node.group(5)
        self.protocol = node.group(3)

        t = re.search(r'remarks=(.*?)(&|$)', node.group(7))
        self.name = f'{self.server}:{self.port}' if not isinstance(t, re.Match) else Base64Decode(t.group(1))

        t = re.search(r'obfsparam=(.*?)(&|$)', node.group(7))
        self.host = None if not isinstance(t, re.Match) else Base64Decode(t.group(1))

        t = re.search(r'protoparam=(.*?)(&|$)', node.group(7))
        self.protocol_param = None if not isinstance(t, re.Match) else Base64Decode(t.group(1))

        self.udp = None

        return self.code()

    def code(self):
        text = f'- name: "{self.name}"\n' +\
            ' '*2 + f'type: ssr\n' +\
            ' '*2 + f'server: {self.server}\n' +\
            ' '*2 + f'port: {self.port}\n' +\
            ' '*2 + f'cipher: {self.cipher}\n' +\
            ' '*2 + f'password: \"{self.password}\"\n' +\
            ' '*2 + f'obfs: {self.obfs}\n' +\
            ' '*2 + f'protocol: {self.protocol}\n'

        if not self.obfs == 'plain' and self.host:
            text += ' '*2 + f'obfs-param: {self.host}\n'
        if not self.protocol == 'origin':
            text += ' '*2 + f'protocol-param: \"{self.protocol_param}\"\n'

        text += ' '*2 + f'udp: {self.udp}'
        return text
