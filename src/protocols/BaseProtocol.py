import abc
import socket
from multiprocessing import Value
from threading import Thread
from time import sleep

class BaseProtocol(metaclass=abc.ABCMeta):


    def __init__(self, ports=list(), bind_ip=None):
        assert isinstance(ports,list), "ports is not a list"
        self.ports = ports
        self.bind_ip = bind_ip

    def scan(self, addrs, output_deque):
        """scans for games on the addresses from the addrs generator and adds
        all found servers to output_deque"""

        # this method defines a receive method that is called in an other thread
        # the receive method runs until a socket timeout happens
        # this happens only when the main process has finished sending because
        # the socket is initialized blocking

        import threading

        sending = Value('i', 0)

        def receive(self, sock, out_deque, sending):
            last_receive = False
            while True:
                try:
                    response = sock.recvfrom(4096)
                    print("response from:", response[1])
                    result = self.parse(response)
                    if result is not None:
                        out_deque.append(result)
                except socket.timeout:
                    if last_receive:
                        return
                    if sending != 0:
                        last_receive = True

        sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        if self.bind_ip is not None:
            socket.bind(self.bind_ip)
        sock.settimeout(2.)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)
        print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))

        receive_thread= Thread(target=receive, daemon=True, args=(self, sock, output_deque, sending))
        receive_thread.start()

        
        for ip in addrs:
            for port in self.ports:
                try:
                    sock.sendto(self.message,(ip,port))
                    sleep(0.02)
                except socket.error:
                    continue
        sending = 1

        receive_thread.join()
        sock.close()

    @abc.abstractmethod
    def parse(self, response):
        """ gets a tuple containing the byte-string that was returned from the
        server and its ip-port-combination"""

