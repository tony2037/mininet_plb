from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.cli import CLI
from utils.benchmark import TESTS
import argparse

parser = argparse.ArgumentParser(description='Script for PLB lab')
parser.add_argument('--topo', default='clos', choices=['ocs', 'clos'])
parser.add_argument('--cli', action='store_true')
args = parser.parse_args()

if args.topo == 'clos':
    from topologies.clos import CLOS as CustomTopo
elif args.topo == 'ocs':
    from topologies.ocs import OCS as CustomTopo
else:
    from topologies.clos import CLOS as CustomTopo

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

def prehookTest(net):
    if args.cli:
        CLI(net)

def performTest(net):
    for test in TESTS:
        test(net)

def posthookTest(net):
    pass

if __name__ == '__main__':
    Cleanup.cleanup()
    net = Mininet( topo = CustomTopo() )
    setupNet(net)
    net.start()

    prehookTest(net)
    performTest(net)
    posthookTest

    net.stop()
    Cleanup.cleanup()
