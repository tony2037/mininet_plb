from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.cli import CLI
from utils.benchmark import TESTS
import argparse

parser = argparse.ArgumentParser(description='Script for PLB lab')
parser.add_argument('--topo', default='clos', choices=['ocs', 'clos', 'test', 'star'])
parser.add_argument('--cli', action='store_true')
args = parser.parse_args()

if args.topo == 'clos':
    from topologies.clos import CLOS as CustomTopo
elif args.topo == 'ocs':
    from topologies.ocs import OCS as CustomTopo
elif args.topo == 'test':
    from topologies.test import Test as CustomTopo
elif args.topo == 'star':
    from topologies.test import StarTopo as CustomTopo
else:
    from topologies.clos import CLOS as CustomTopo

def setupNode(node):
    # net.ipv4.tcp_plb_cong_thresh=32 -> 32/(2^8) = 0.125, threshold for CE fraction
    setupCmds = ['sudo sysctl -w net.ipv4.tcp_ecn=1', \
                 'sudo sysctl -w net.ipv4.tcp_congestion_control=cubic',\
                 'sudo sysctl -w net.ipv4.tcp_plb_enabled=1',\
                 'sudo sysctl -w net.ipv4.tcp_plb_cong_thresh=32',\
                 'sudo sysctl -w net.ipv4.tcp_plb_rehash_rounds=3',\
                 'sudo sysctl -w net.core.default_qdisc=fq',\
                 'sudo sysctl --system'\
    ]
    interfaces = node.intfNames()
    for interface in interfaces:
        node.cmd(f'tc qdisc change dev {interface} root red limit 100000 min 2000 max 10000 avpkt 100 burst 21 ecn')
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
    if args.cli:
        CLI(net)

if __name__ == '__main__':
    Cleanup.cleanup()
    net = Mininet( topo = CustomTopo() )
    setupNet(net)
    net.start()

    prehookTest(net)
    performTest(net)
    posthookTest(net)

    net.stop()
    Cleanup.cleanup()
