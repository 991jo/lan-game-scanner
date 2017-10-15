import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class Quake3Protocol(BaseProtocol):

    def __init__(self, ports=[27070, 27960, 27961, 27962, 27963, 27992, 28960, 28961, 28962, 28963]):
        # the XXXX0-3 Ports are used because many people host multiple server on ascending ports
        super().__init__(ports=ports)

    def scan(self, nets):
        results = list()

        # 0xFF0xFF0xFF0xFFgetstatus\n
        MESSAGE = bytearray([0xFF, 0xFF, 0xFF,0xFF, 0x67, 0x65, 0x74, 0x73, 0x74, 0x61, 0x74, 0x75, 0x73, 0x0A])

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
                sender = response[1]
                data = [m.split(b'\\') for m in response[0].splitlines(0x0A)]

                # check if the response is correct
                header = data[0][0]
                header_template = b"\xFF\xFF\xFF\xFFstatusResponse\n"
                if header != header_template:
                    continue

                response_dict = dict()

                # build a dict from the response
                # first entry in data[1] is empty, has to be skipped
                # then every 2 entries are a key value pair.
                i = 1
                while i < len(data[1]):
                    key = data[1][i].decode().lower() #lowered because some servers reply with some fields not all lower case
                    value = data[1][i+1].decode()
                    response_dict[key] = value
                    i+=2

                player_count = len(data[2:])

                server_dict = dict()
                server_dict["ip"] = sender[0]
                server_dict["hostname"] = None
                server_dict["port"] = sender[1]
                server_dict["server_name"] = response_dict["sv_hostname"]
                server_dict["map"] = response_dict["mapname"]
                server_dict["max_players"] = response_dict["sv_maxclients"]
                server_dict["players"] = player_count
                server_dict["game"] = response_dict["gamename"]
                server_dict["game_type"] = response_dict["g_gametype"]

                results.append(server_dict)
            # if the socket timeout is triggered no packet have been received in the last 5 seconds
            except socket.timeout: 
                break
        sock.close()

        return results
