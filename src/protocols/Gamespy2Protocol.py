import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class Gamespy2Protocol(BaseProtocol):

    def __init__(self, ports=[2302,2303,2304,2304,2305,23000,1717]):
        # those ports are probably to many
        super().__init__(ports=ports)

    def scan(self, nets):

        # Gamespy Protocol 
        # http://int64.org/docs/gamestat-protocols/gamespy.html
        results = list()

        MESSAGE = bytearray([0xFE, 0xFD, 0x00, 0x43, 0x4F, 0x52, 0x59, 0xFF, 0xFF, 0x00] )


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

        pp = PrettyPrinter()
        header_expected = b'\x00CORY'
        while True:
            try:
                response = sock.recvfrom(4096)
                data = response[0]
                sender = response[1]

                header = data[:5]
                if header != header_expected:
                    print("Header missmatch")
                    print(response)
                    continue

                payload = data[5:].split(b'\x00')
#                pp.pprint(payload)

                response_dict = dict()

                # build a dict from the response
                i = 0
                while i < len(payload) - 1:
                    key = payload[i].decode().lower() #lowered because some servers reply with some fields not all lower case
                    value = payload[i+1]
                    response_dict[key] = value
                    i+=2

                pp.pprint(response_dict)

                server_dict = dict()
                server_dict["ip"] = sender[0]
                server_dict["hostname"] = None
                server_dict["port"] = response_dict["hostport"].decode()
                server_dict["server_name"] = response_dict["hostname"].decode("utf-8","ignore")
                server_dict["map"] = response_dict["mapname"].decode("utf-8","ignore")
                server_dict["max_players"] = response_dict["maxplayers"].decode("utf-8","ignore")
                server_dict["players"] = response_dict["numplayers"].decode("utf-8","ignore")
                if "game_id" in response_dict:
                    server_dict["game"] = response_dict["game_id"].decode("utf-8","ignore")
                elif "gamename" in response_dict:
                    server_dict["game"] = response_dict["gamename"].decode("utf-8","ignore")
                else:
                    server_dict["game"] = "unknown"
                server_dict["game_type"] = None


                results.append(server_dict)
            # if the socket timeout is triggered no packet have been received in the last 5 seconds
            except socket.timeout: 
                break
        sock.close()

        return results
