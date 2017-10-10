from queue import Queue
from collections import deque

from time import sleep
import threading

from protocols.SRCDSProtocol import SRCDSProtocol
class WorkerPool():

    def __init__(self, protocol_pool, num_worker_threads=10):
        self.protocol_pool = protocol_pool
        self.srcds = SRCDSProtocol()
        self.num_worker_threads = num_worker_threads

    def scan(self,ips):
        in_queue = Queue()
        out_deque = deque()

        def worker():
            while True:
                ip = in_queue.get()
                if ip is None:
                    break
                out_deque.extend(self.protocol_pool.scan(ip))
                in_queue.task_done()

        threads = list()
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        for ip in ips:
            in_queue.put(ip)

        in_queue.join()
        for i in range(self.num_worker_threads):
            in_queue.put(None)
        for t in threads:
            t.join()

        return list(out_deque)
