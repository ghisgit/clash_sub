import re
import urllib.parse


class TrojanNode():
    def __init__(self, link, host=None, udp=None, in_node=[], out_node=[]) -> None:
        xq = re.match (r'trojan://(.*?)@(.*?):(.*?)\?(.*?)#(.*)', link)
        if isinstance(xq, re.Match):
            self.__data = ''
            self.out_node = ['剩余流量', '过期时间'] + out_node
            self.in_node = in_node

            self.name = urllib.parse.unquote(xq.group(5))
            self.type = 'trojan'
            self.server = xq.group(2)
            self.port = xq.group(3)
            self.password = xq.group(1)
            self.udp = 'true' if udp==1 else 'false'

            t = re.search(r'peer=(.*?)(&|#)', xq.group(4))
            sni = self.server if not isinstance(t, re.Match) else t.group(1)
            self.sni = host if host else sni
            self.scv = 'true' if host else 'flase'
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
        self.__data += (' '*2 + f'password: \"{self.password}\"\n')
        self.__data += (' '*2 + f'udp: {self.udp}\n')
        self.__data += (' '*2 + f'sni: {self.sni}\n')
        self.__data += (' '*2 + f'skip-cert-verify: {self.scv}')
        return self.__data

    @property
    def node(self):
        return self.__str__()
