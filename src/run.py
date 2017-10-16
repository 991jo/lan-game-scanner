from pprint import PrettyPrinter

#import WorkerPool
#from ProtocolPool import ProtocolPool
#from IPGenerator import generate
from protocols.SRCDSProtocol import SRCDSProtocol
from protocols.Quake3Protocol import Quake3Protocol
from protocols.MumbleProtocol import MumbleProtocol

from outputs import export_json, export_gns


nets = ["92.51.148.185/32","91.189.221.186/32","91.245.218.9/32"]


srcds = SRCDSProtocol()
q3 = Quake3Protocol()
mumble = MumbleProtocol()
protocols = [srcds, q3, mumble]

results = list()
for p in protocols:
    results.extend(p.scan(nets))

pp = PrettyPrinter(indent=2)
pp.pprint(results)
export_json.export(results, "./output.json")
export_gns.export(results, "./output_gns.json")

