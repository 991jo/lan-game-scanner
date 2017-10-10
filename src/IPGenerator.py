from ipaddress import ip_network

def generate(nets):
    for net in nets:
        ipnet = ip_network(net)
        for ip in ipnet:
            yield str(ip)
