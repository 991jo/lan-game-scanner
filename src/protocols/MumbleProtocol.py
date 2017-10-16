import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class MumbleProtocol(BaseProtocol):

    def __init__(self, ports=[64738]):
        # are there further ports often used by mumble?
        super().__init__(ports=ports)

    def scan(self, nets):
        results = list()
        # https://wiki.mumble.info/wiki/Protocol
        # 4 bytes int       0         -> request type
        # 8 bytes longlong  ident     -> used to identify responses, here just a FF00FF00 pattern  
        MESSAGE = bytearray([0x00, 0x00, 0x00,0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00])

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
                data = response[0]

                if len(data) < 24:
                    # packet does not have minimum length
                    continue

                version = data[0:4]
                ident = data[4:12]
                user_count = int(data[12:16].hex(), base=16)
                slot_count = int(data[16:20].hex(), base=16)
                bandwidth = int(data[20:24].hex(), base=16)

                # check if the response is correct
                ident_expected = b"\xff\x00\xff\x00\xff\x00\xff\x00"
                if ident != ident_expected:
                    print(ident)
                    print(ident_expected)
                    continue

                server_dict = dict()
                server_dict["ip"] = sender[0]
                server_dict["hostname"] = None
                server_dict["port"] = sender[1]
                server_dict["server_name"] = sender[0] + ":" + str(sender[1])
                server_dict["map"] = None
                server_dict["max_players"] = slot_count
                server_dict["players"] = user_count 
                server_dict["game"] = "Mumble" 
                server_dict["game_type"] = "Mumble"

                results.append(server_dict)
            # if the socket timeout is triggered no packet have been received in the last 5 seconds
            except socket.timeout: 
                break
        sock.close()

        return results
