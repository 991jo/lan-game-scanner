import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class GamespyProtocol(BaseProtocol):

    def __init__(self, ports=[7777, 7778, 7787, 7788, 23000]):
        # those ports are probably to many
        super().__init__(ports=ports)

    def scan(self, nets):

        # Gamespy Protocol 
        # http://int64.org/docs/gamestat-protocols/gamespy.html
        results = list()

        # 0xFF0xFF0xFF0xFFgetstatus\n
        MESSAGE = bytearray([0x5C, 0x69, 0x6E, 0x66, 0x6F, 0x5C] )

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5) # the socket timeout might be decreased then in a LAN
        # increase the buffer size of the network, because it might be to slow.
        # Also probably needs to be adjusted in the OS
        # for linux it is e.g
        # sysctl -w net.core.rmem_max=1048576
        # this increases the buffer to 1MB
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)

        for net in nets:
            for ip in ipaddress.ip_network(net):
                ip_str = str(ip)
                for port in self.ports:
                    sock.sendto(MESSAGE,(ip_str,port))
                    sleep(0.001) # for rate limiting, because it may overwhelm some devices on the network path

        while True:
            try:
                response = sock.recvfrom(4096)
                data = response[0]
                sender = response[1]

                if len(data) < 4:
                    continue

                data_split = data.split(b"\\")[1:-1]
#                print(data_split)

                response_dict = dict()

                # build a dict from the response
                # first entry in data[1] is empty, has to be skipped
                # then every 2 entries are a key value pair.
                i = 0
                while i < len(data_split) - 1:
                    key = data_split[i].decode().lower() #lowered because some servers reply with some fields not all lower case
                    value = data_split[i+1]
                    response_dict[key] = value
                    i+=2

                print(response_dict)
                continue

                player_count = len(data[2:])

                server_dict = dict()
                server_dict["ip"] = sender[0]
                server_dict["hostname"] = None
                server_dict["port"] = response_dict["hostport"]
                server_dict["server_name"] = response_dict["hostname"]
                server_dict["map"] = response_dict["mapname"]
                server_dict["max_players"] = response_dict["maxplayers"]
                server_dict["players"] = response_dict["maxplayers"]
                server_dict["game"] = response_dict["gamename"]
                server_dict["game_type"] = response_dict["g_gametype"]

                results.append(server_dict)
            # if the socket timeout is triggered no packet have been received in the last 5 seconds
            except socket.timeout: 
                break
        sock.close()

        return results
