from queue import Queue
from collections import deque

import threading

class ProtocolPool:

    def __init__(self, protocols=None, num_worker_threads=5):
        assert isinstance(protocols, list), "protocols needs to be a list of protocol-instances"

        self.protocols = protocols
        self.num_worker_threads = num_worker_threads

    def scan(self, ip):
        in_queue = Queue()
        out_deque = deque()

        def worker():
            while True:
                proto = in_queue.get()
                if proto is None:
                    break
                out_deque.extend(proto.scan(ip))
                in_queue.task_done()

        threads = list()
        for i in range(self.num_worker_threads):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        for p in self.protocols:
            in_queue.put(p)

        in_queue.join()
        
        for i in range(self.num_worker_threads):
            in_queue.put(None)

        for t in threads:
            t.join()

        return out_deque
