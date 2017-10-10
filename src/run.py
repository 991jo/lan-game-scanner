from pprint import PrettyPrinter

import WorkerPool
from ProtocolPool import ProtocolPool
from IPGenerator import generate
from protocols.SRCDSProtocol import SRCDSProtocol
from protocols.Quake3Protocol import Quake3Protocol

from outputs import export_json, export_gns


#nets = ["213.202.223.128/25", "92.51.148.160/27"]
nets = ["51.255.25.199/32","92.222.182.117/32", "87.117.203.203/32","162.248.92.171/32", "45.76.94.34/32"]
srcds = SRCDSProtocol()
q3 = Quake3Protocol()
ProtoPool = ProtocolPool([srcds,q3])

p = WorkerPool.WorkerPool(ProtoPool, num_worker_threads = 10)
result = p.scan(generate(nets))

pp = PrettyPrinter(indent=2)
#pp.pprint(result)
export_json.export(result, "./output.json")
export_gns.export(result, "./output_gns.json")

