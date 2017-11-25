import socket
import ipaddress
from time import sleep
from pprint import PrettyPrinter

from protocols.BaseProtocol import BaseProtocol

class GamespyProtocol(BaseProtocol):

    def __init__(self, ports=[7777, 7778, 7787, 7788, 23000], bind_ip=None):
        # those ports are probably to many
        super().__init__(ports=ports, bind_ip=bind_ip)

        self.message = bytearray([0x5C, 0x69, 0x6E, 0x66, 0x6F, 0x5C] )


    def parse(self, response):
        data = response[0]
        sender = response[1]

        if len(data) < 4:
            return

        data_split = data.split(b"\\")[1:-1]

        response_dict = dict()

        # build a dict from the response
        # first entry in data[1] is empty, has to be skipped
        # then every 2 entries are a key value pair.
        i = 0
        while i < len(data_split) - 1:
            key = data_split[i].decode().lower() #lowered because some servers reply with some fields not all lower case
            value = data_split[i+1].decode('utf-8','ignore')
            response_dict[key] = value
            i+=2

        print(response_dict)

        player_count = len(data[2:])

        server_dict = dict()
        server_dict["ip"] = sender[0]
        server_dict["hostname"] = None
        server_dict["port"] = response_dict["hostport"]
        server_dict["server_name"] = response_dict["hostname"]
        server_dict["map"] = response_dict["mapname"]
        server_dict["max_players"] = response_dict["maxplayers"]
        server_dict["players"] = response_dict["numplayers"]
        server_dict["game"] = response_dict["gameid"]
        server_dict["game_type"] = response_dict["gametype"]

        return(server_dict)

