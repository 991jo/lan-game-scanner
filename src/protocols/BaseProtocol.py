import abc

class BaseProtocol(metaclass=abc.ABCMeta):


    def __init__(self, ports=list()):
        assert isinstance(ports,list), "ports is not a list"
        self.ports = ports

    def add_ports(self, ports):
        assert isinstance(ports,list), "ports is not a list"
        self.ports.extend(ports)

    @abc.abstractmethod
    def scan(self, ip):
        """Scans the given IP on the ports defined for the protocol and returns
        a list of dicts containing the found servers. If no servers are found 
        this list is empty"""
