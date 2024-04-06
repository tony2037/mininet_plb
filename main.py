from mininet.clean import Cleanup
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import time
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
    # net.ipv4.tcp_plb_cong_thresh=32 -> 32/(2^8) = 0.125, threshold for CE fraction
    setupCmds = ['sudo sysctl -w net.ipv4.tcp_ecn=1', \
                 'sudo sysctl -w net.ipv4.tcp_congestion_control=dctcp',\
                 'sudo sysctl -w net.ipv4.tcp_plb_enabled=1',\
                 'sudo sysctl -w net.ipv4.tcp_plb_cong_thresh=32',\
                 'sudo sysctl -w net.ipv4.tcp_plb_rehash_rounds=3',\
                 'sudo sysctl --system'\
    ]
    for setupCmd in setupCmds:
        node.cmd(setupCmd)

def setupNet(net):
    nodes = net.values()
    for node in nodes:
        setupNode(node)

def iperf():
    server = net.get('A1_T0_h0')
    client = net.get('A0_T0_h0')
    server.cmd('iperf -s &')
    time.sleep(1)
    iperf_results = client.cmd(f'iperf -c A1_T0_h0 -t 10 -b 10M -i 1')
    print(iperf_results)

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
    net = Mininet( topo = CustomTopo(), link = TCLink )
    setupNet(net)
    net.start()

    iperf()

    prehookTest(net)
    performTest(net)
    posthookTest

    net.stop()
    Cleanup.cleanup()
