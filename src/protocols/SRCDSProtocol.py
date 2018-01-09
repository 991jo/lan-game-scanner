from protocols.BaseProtocol import BaseProtocol

class SRCDSProtocol(BaseProtocol):

    def __init__(self, ports=[27015,27016,27017, 27018, 27019], bind_ip=None):
        super().__init__(ports=ports, bind_ip=bind_ip)

        # 0xFF0xFF0xFF0xFFTSource Engine Query.
        message = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0x54, 0x53, 0x6F, 0x75,
                    0x72, 0x63, 0x65, 0x20, 0x45, 0x6E, 0x67, 0x69, 0x6E,
                    0x65, 0x20, 0x51, 0x75, 0x65, 0x72, 0x79, 0x00])
        self.message = message



    def parse(self, response):
        sender = response[1]
        data = response[0][4:]

        server_dict = dict()

        server_dict["ip"] = sender[0]
        server_dict["port"] = sender[1]
        server_dict["hostname"] = None

        header                      = data[0] #Header
        if header != 0x49:
            print(data)
            return
        payload                     = data[2:] # Name
        name_end                    = payload.find(b"\x00")
        server_dict["server_name"]  = payload[0:name_end].decode('utf-8', 'ignore')  # Name
        mapname_end                 = payload.find(b"\x00",name_end+1)
        server_dict["map"]          = payload[name_end+1:mapname_end].decode('utf-8', 'ignore') # Map
        folder_end                  = payload.find(b"\x00",mapname_end+1)
        server_dict["game"]         = payload[mapname_end + 1: folder_end].decode('utf-8', 'ignore') # Folder
        game_end                    = payload.find(b"\x00",folder_end+1)
        server_dict["gametype"]     = payload[folder_end + 1: game_end].decode('utf-8', 'ignore') # Game
        # game_id                   = payload[game_end+1: game_end+3] # ID
        server_dict["players"]      = int.from_bytes(payload[game_end+3:game_end+4],byteorder='little') # Players
        server_dict["max_players"]  = int.from_bytes(payload[game_end+4:game_end+5], byteorder='little') # Max. Players
        # bot_count                 = payload[game_end+5:game_end+6] # Bots
        # server_type               = payload[game_end+6:game_end+7] # Server Type
        # environment               = payload[game_end+7:game_end+8] # Environment
        # visibility                = payload[game_end+8:game_end+9] # Visibility
        # vac                       = payload[game_end+9:game_end+10] # VAC

        return server_dict

        
