from pprint import PrettyPrinter

#import WorkerPool
#from ProtocolPool import ProtocolPool
#from IPGenerator import generate
from protocols.SRCDSProtocol import SRCDSProtocol
from protocols.Quake3Protocol import Quake3Protocol
from protocols.MumbleProtocol import MumbleProtocol
from protocols.Gamespy2Protocol import Gamespy2Protocol

from outputs import export_json, export_gns


nets = ["92.51.148.0/24","91.189.221.0/24","91.245.218.0/24","46.174.53.0/24","213.238.173.0/24"]
nets.extend(["73.37.176.0/20"])
nets.extend(["208.167.232.0/24","217.23.5.0/24","188.32.101.0/24","162.248.88.0/24"])


srcds = SRCDSProtocol()
q3 = Quake3Protocol()
mumble = MumbleProtocol()
gs2 = Gamespy2Protocol()
protocols = [srcds, q3, mumble, gs2]

results = list()
for p in protocols:
    results.extend(p.scan(nets))

pp = PrettyPrinter(indent=2)
pp.pprint(results)
export_json.export(results, "./output.json")
export_gns.export(results, "./output_gns.json")

