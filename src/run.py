from pprint import PrettyPrinter

import WorkerPool
from ProtocolPool import ProtocolPool
from IPGenerator import generate
from protocols.SRCDSProtocol import SRCDSProtocol

from outputs import export_json, export_gns


nets = ["213.202.223.128/25", "92.51.148.160/27"]

srcds = SRCDSProtocol()
ProtoPool = ProtocolPool([srcds])

p = WorkerPool.WorkerPool(ProtoPool, num_worker_threads = 40)
result = p.scan(generate(nets))

pp = PrettyPrinter(indent=2)
#pp.pprint(result)
export_json.export(result, "./output.json")
export_gns.export(result, "./output_gns.json")

