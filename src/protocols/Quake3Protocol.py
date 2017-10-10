import socket
from multiprocessing import Pool

from protocols.BaseProtocol import BaseProtocol

class Quake3Protocol(BaseProtocol):

    def __init__(self, ports=[27070, 27960, 27992, 28960]):
        super().__init__(ports=ports)

    def _scan_port_(self, ip_port):
        """Scans the ip_port tuple and returns a dict if a gameserver was found or None if not."""
        try:
            MESSAGE = bytearray([0xFF, 0xFF, 0xFF,0xFF, 0x67, 0x65, 0x74, 0x73, 0x74, 0x61, 0x74, 0x75, 0x73, 0x0A])
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(MESSAGE,ip_port)
            response = sock.recvfrom(4096)
            response = [m.split(b'\\') for m in response[0].splitlines(0x0A)]

            response_dict = dict()

            i = 1
            while i < len(response[1]):
                key = response[1][i].decode()
                value = response[1][i+1].decode()
                response_dict[key] = value
                i+=2


            player_count = len(response[2:])

            server_dict = dict()
            server_dict["ip"] = ip_port[0]
            server_dict["hostname"] = None
            server_dict["port"] = ip_port[1]
            server_dict["server_name"] = response_dict["sv_hostname"]
            server_dict["map"] = response_dict["mapname"]
            server_dict["max_players"] = response_dict["sv_maxclients"]
            server_dict["players"] = player_count
            server_dict["game"] = response_dict["gamename"]
            server_dict["game_type"] = response_dict["g_gametype"]

            return server_dict

        except socket.timeout:
            pass
        finally:
            sock.close()

    def scan(self, ip):
        results = list()

        ip_ports = zip([ip]*len(self.ports),self.ports)

        with Pool(len(self.ports)) as p:
            results = p.map(self._scan_port_, ip_ports)

        return filter(lambda x: x is not None, results)
