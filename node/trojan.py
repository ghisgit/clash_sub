import re

from urllib.parse import unquote


class Trojan():
    def __init__(self, link, udp, cert, host):
        self.link = link
        self.__udp = udp
        self.__cert = cert
        self.__host = host

    def parse(self):
        node = re.match('^(.*?)@(.*?):(.*?)\?(.*?)#(.*)$', self.link)
        self.name = unquote(node.group(5))
        self.server = node.group(2)
        self.port = node.group(3)
        self.password = node.group(1)

        t = re.search(r'(sni)|(peer)=(.*?)(&|$)', node.group(4))
        self.host = None if not isinstance(t, re.Match) else t.group(3)
        self.udp = None
        t = re.search(r'allowInsecure=(.*?)(&|$)', node.group(4))
        self.cert = 1 if not isinstance(t, re.Match) else t.group(1)

        return self.code()

    def code(self):
        text = f'- name: "{self.name}"\n' +\
            ' ' * 2 + 'type: trojan\n' +\
            ' ' * 2 + f'server: {self.server}\n' +\
            ' ' * 2 + f'port: {self.port}\n' +\
            ' ' * 2 + f'password: {self.password}\n' +\
            ' ' * 2 + f'udp: {self.udp}\n' +\
            ' ' * 2 + f'sni: {self.host}\n' +\
            ' ' * 2 + f'skip-cert-verify: {self.cert}'
        return text


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
    def cert(self):
        if self.__cert == 1:
            return 'true'
        elif self.__cert == -1:
            return 'false'

    @cert.setter
    def cert(self, value):
        if self.__cert == 0:
            self.__cert = -1 if int(value) == 0 else 1

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = self.__host if self.__host else value
