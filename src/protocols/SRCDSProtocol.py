from multiprocessing import Pool

from protocols.BaseProtocol import BaseProtocol
from valve.source.a2s import ServerQuerier
from valve.source import NoResponseError
from valve.source.messages import BrokenMessageError

class SRCDSProtocol(BaseProtocol):

    def __init__(self, ports=[27015,27016,27017, 27018, 27019]):
        super().__init__(ports=ports)

    def _scan_port_(self, ip_port):
        """Scans the ip_port tuple and returns a dict if a gameserver was found or None if not."""
        try:
            server = ServerQuerier(ip_port)
            info = server.info()
            server_dict = dict()
            server_dict["ip"] = ip_port[0]
            server_dict["hostname"] = None
            server_dict["port"] = ip_port[1]
            server_dict["server_name"] = info["server_name"]
            server_dict["map"] = info["map"]
            server_dict["max_players"] = info["max_players"]
            server_dict["players"] = info["player_count"]
            server_dict["game"] = info["folder"]
            server_dict["game_type"] = info["game"]

            return server_dict

        except (NoResponseError, BrokenMessageError):
            pass
        finally:
            server.close()

    def scan(self, ip):
        print("ports:", self.ports)
        results = list()

        ip_ports = zip([ip]*len(self.ports),self.ports)

        with Pool(len(self.ports)) as p:
            results = p.map(self._scan_port_, ip_ports)

        return filter(lambda x: x is not None, results)
