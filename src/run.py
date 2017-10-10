import WorkerPool
from ProtocolPool import ProtocolPool
from protocols.SRCDSProtocol import SRCDSProtocol
from pprint import PrettyPrinter

ips = ['213.202.223.248',
 '213.202.228.149',
 '213.202.228.70',
 '213.202.229.109',
 '213.202.229.154',
 '213.202.229.76',
 '213.202.230.104',
 '213.239.196.115',
 '213.239.199.140',
 '213.239.221.114',
 '217.11.249.84',
 '217.160.142.142',
 '217.172.172.37',
 '217.182.197.116',
 '217.198.133.123',
 '217.79.188.144',
 '217.79.188.156',
 'cwclan.de',
 '217.79.188.212']

srcds = SRCDSProtocol()
ProtoPool = ProtocolPool([srcds])


p = WorkerPool.WorkerPool(ProtoPool, num_worker_threads = 20)
result = p.scan(ips)

pp = PrettyPrinter(indent=2)
pp.pprint(result)
