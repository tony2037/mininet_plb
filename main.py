from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.cli import CLI

from topologies.ocs import OCS as CustomTopo
from utils.benchmark import TESTS

def setupNode(node):
    setupCmds = ['sysctl -w net.ipv4.tcp_congestion_control=bbr',\
                    'sysctl -w net.ipv4.tcp_plb_enabled=1'\
                    'sudo sysctl --system'\
    ]
    for setupCmd in setupCmds:
        node.cmd(setupCmd)

def setupNet(net):
    nodes = net.values()
    for node in nodes:
        setupNode(node)

if __name__ == '__main__':
    Cleanup.cleanup()
    net = Mininet( topo = CustomTopo() )
    setupNet(net)
    net.start()

    for test in TESTS:
        test(net)

    net.stop()
    Cleanup.cleanup()