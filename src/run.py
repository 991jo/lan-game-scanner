import ipaddress
import collections
import config 
from multiprocessing import Manager, Process
from pprint import PrettyPrinter

from protocols.SRCDSProtocol import SRCDSProtocol
from protocols.Quake3Protocol import Quake3Protocol
from protocols.MumbleProtocol import MumbleProtocol
from protocols.GamespyProtocol import GamespyProtocol
from protocols.Gamespy2Protocol import Gamespy2Protocol

#from outputs import export_json, export_gns

cfg = config.read_config()

ips = list()
ips.extend(cfg.options('ips'))
for network in cfg.options('networks'):
    ips.extend(str(ip) for ip in ipaddress.ip_network(network, strict=False))

srcds = SRCDSProtocol()
q3 = Quake3Protocol()
mumble = MumbleProtocol()
gs = GamespyProtocol()
gs2 = Gamespy2Protocol()
protocols = [q3,srcds, mumble, gs, gs2]

with Manager() as manager:

    output_list = manager.list()

    processes = list()
    for p in protocols:
        proc = Process(target=p.scan, daemon=True, args=(ips, output_list))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    pp = PrettyPrinter(indent=2)
    output = list(output_list)
    pp.pprint(output)
    pp.pprint(len(output))

