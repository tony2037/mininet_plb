from mininet.clean import Cleanup
from mininet.net import Mininet

from topologies.ocs import OCS as CustomTopo
from utils.benchmark import TESTS


if __name__ == '__main__':
    Cleanup.cleanup()
    net = Mininet( topo = CustomTopo() )
    net.start()

    for test in TESTS:
        test(net)

    net.stop()
    Cleanup.cleanup()