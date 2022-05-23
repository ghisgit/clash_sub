import re

from node.BaseParse import base64_decode

class SsrNode():
    def __init__(self, link, host=None, udp=None, in_node=[], out_node=[]) -> None:
        xq = re.match (r'ssr://(.*)', link)
        if isinstance(xq, re.Match):
            xq = re.match(r'(.*?):(.*?):(.*?):(.*?):(.*?):(.*?)/\?(.*)', base64_decode(xq.group(1)))
            self.__data = ''
            self.out_node = ['剩余流量', '过期时间'] + out_node
            self.in_node = in_node

            self.type = 'ssr'
            self.server = xq.group(1)
            self.port = xq.group(2)
            self.cipher = xq.group(4)
            self.password = base64_decode(xq.group(6))
            self.obfs = xq.group(5)
            self.protocol = xq.group(3)

            t = re.search(r'remarks=(.*?)(&|$)', xq.group(7))
            name = f'{self.server}:{self.port}' if not isinstance(t, re.Match) else base64_decode(t.group(1))
            self.name = name

            t = re.search(r'obfsparam=(.*?)(&|$)', xq.group(7))
            obfs_param = self.server if not isinstance(t, re.Match) else base64_decode(t.group(1))
            self.obfs_param= host if host else obfs_param

            t = re.search(r'protoparam=(.*?)(&|$)', xq.group(7))
            protocol_param = None if not isinstance(t, re.Match) else base64_decode(t.group(1))
            self.protocol_param= protocol_param

            self.udp = 'true' if udp==1 else 'false'
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
        self.__data += (' '*2 + f'cipher: {self.cipher}\n')
        self.__data += (' '*2 + f'password: \"{self.password}\"\n')
        self.__data += (' '*2 + f'obfs: {self.obfs}\n')
        self.__data += (' '*2 + f'protocol: {self.protocol}\n')

        if not self.obfs == 'plain':
            self.__data += (' '*2 + f'obfs-param: {self.obfs_param}\n')
        if not self.protocol == 'origin':
            self.__data += (' '*2 + f'protocol-param: \"{self.protocol_param}\"\n')

        self.__data += (' '*2 + f'udp: {self.udp}')
        return self.__data

    @property
    def node(self):
        return self.__str__()
