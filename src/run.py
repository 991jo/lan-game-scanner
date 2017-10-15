from pprint import PrettyPrinter

from protocols.SRCDSProtocol import SRCDSProtocol
from protocols.Quake3Protocol import Quake3Protocol

from outputs import export_json, export_gns


nets = ["213.202.223.128/25", "92.51.148.160/27"]
nets.extend(['84.200.101.114/32', '83.233.46.187/32', '188.116.46.134/32', '68.232.181.21/32', '148.251.167.15/32', '107.191.126.11/32', '69.28.210.30/32', '216.158.234.228/32', '190.112.0.109/32', '136.144.141.127/32', '84.200.223.179/32'])

srcds = SRCDSProtocol()
q3 = Quake3Protocol()

result = q3.scan(nets)
result.extend(srcds.scan(nets))

pp = PrettyPrinter(indent=2)
pp.pprint(result)
export_json.export(result, "./output.json")
export_gns.export(result, "./output_gns.json")

