from protocols.BaseProtocol import BaseProtocol

class MumbleProtocol(BaseProtocol):

    def __init__(self, ports=[64738], bind_ip=None):
        # are there further ports often used by mumble?
        super().__init__(ports=ports, bind_ip=bind_ip)

        self.message = bytearray([0x00, 0x00, 0x00,0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00, 0xFF, 0x00])

    def parse(self, response):
        sender = response[1]
        data = response[0]

        if len(data) < 24:
            # packet does not have minimum length
            return

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
            return

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

        return server_dict
