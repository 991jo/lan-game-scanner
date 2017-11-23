import socket
import ipaddress
from time import sleep

from protocols.BaseProtocol import BaseProtocol
#from multiprocessing import Pool

#from protocols.BaseProtocol import BaseProtocol
#from valve.source.a2s import ServerQuerier
#from valve.source import NoResponseError
#from valve.source.messages import BrokenMessageError

class SRCDSProtocol(BaseProtocol):

    def __init__(self, ports=[27015,27016,27017, 27018, 27019]):
        super().__init__(ports=ports)

    def scan(self, nets):
        results = list()

        # 0xFF0xFF0xFF0xFFTSource Engine Query.
        MESSAGE = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0x54, 0x53, 0x6F, 0x75,
                    0x72, 0x63, 0x65, 0x20, 0x45, 0x6E, 0x67, 0x69, 0x6E,
                    0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00])


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
                    try:
                        sock.sendto(MESSAGE,(ip_str,port))
                    except socket.error as e:
                        # sometimes there might be a socket error
                        # e.g. when you are sending to a broadcast address
                        # which happens when you are scanning a supernet of a
                        # network the host is attached to
                        # Sending to broadcast-adsresses in other networks should
                        # be fine, because you don't know it's a broadcast address
                        pass
                    sleep(0.001) # for rate limiting, because it may overwhelm some devices on the network path

        while True:
            try:
                response = sock.recvfrom(4096)
                sender = response[1]
                data = response[0][4:]

                server_dict = dict()

                server_dict["ip"] = sender[0]
                server_dict["port"] = sender[1]
                server_dict["hostname"] = None
        
                header                      = data[0] #Header
                if header != 0x49:
                    continue

                #protocol                   = data[1] #Protocol
                payload                     = data[2:] # Name
                name_end                    = payload.find(b"\x00")
                server_dict["server_name"]  = payload[2:name_end].decode('utf-8', 'ignore')  # Name
                mapname_end                 = payload.find(b"\x00",name_end+1)
                server_dict["map"]          = payload[name_end+1:mapname_end].decode('utf-8', 'ignore') # Map
                folder_end                  = payload.find(b"\x00",mapname_end+1)
                server_dict["game"]         = payload[mapname_end + 1: folder_end].decode('utf-8', 'ignore') # Folder
                game_end                    = payload.find(b"\x00",folder_end+1)
                server_dict["game_type"]     = payload[folder_end + 1: game_end].decode('utf-8', 'ignore') # Game
                # game_id                   = payload[game_end+1: game_end+3] # ID
                server_dict["players"]      = int.from_bytes(payload[game_end+3:game_end+4],byteorder='little') # Players
                server_dict["max_players"]  = int.from_bytes(payload[game_end+4:game_end+5], byteorder='little') # Max. Players
                # bot_count                 = payload[game_end+5:game_end+6] # Bots
                # server_type               = payload[game_end+6:game_end+7] # Server Type
                # environment               = payload[game_end+7:game_end+8] # Environment
                # visibility                = payload[game_end+8:game_end+9] # Visibility
                # vac                       = payload[game_end+9:game_end+10] # VAC

                results.append(server_dict)
            # if the socket timeout is triggered no packet have been received in the last 5 seconds
            except socket.timeout: 
                break
        sock.close()

        return results

