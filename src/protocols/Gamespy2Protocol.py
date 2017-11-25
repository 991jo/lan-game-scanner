import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class Gamespy2Protocol(BaseProtocol):

    def __init__(self, ports=[2302,2303,2304,2304,2305,23000,1717], bind_ip=None):
        # those ports are probably to many
        super().__init__(ports=ports, bind_ip=bind_ip)

        self.message = bytearray([0xFE, 0xFD, 0x00, 0x43, 0x4F, 0x52, 0x59, 0xFF, 0xFF, 0x00] )

    def parse(self, response):
                data = response[0]
                sender = response[1]

                header = data[:5]
                header_expected = b'\x00CORY'
                if header != header_expected:
                    print("Header missmatch")
                    print(response)
                    return

                payload = data[5:].split(b'\x00')

                response_dict = dict()

                # build a dict from the response
                i = 0
                while i < len(payload) - 1:
                    key = payload[i].decode().lower() #lowered because some servers reply with some fields not all lower case
                    value = payload[i+1]
                    response_dict[key] = value
                    i+=2

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
