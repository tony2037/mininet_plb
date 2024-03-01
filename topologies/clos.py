from .base import Base

class CLOS( Base ):
    def build(self, numSpines=2, numAggrs=4, numTor=4, hostsPerTor=2):
        # Add Spine Switches
        spineSwitches = [self.addStpSwitch(f's{i}') for i in range(1, numSpines + 1)]

        # Add Aggr Switches
        aggrSwitches = [self.addStpSwitch(f'a{i}') for i in range(1, numAggrs + 1)]

        # Connect each Leaf Switch to all Spine Switches
        for leaf in aggrSwitches:
            for spine in spineSwitches:
                self.addLink(leaf, spine)

        # Add ToRs and connect to Aggr Switches
        torCount = 1
        torSwitches = []
        for leaf in aggrSwitches:
            for _ in range(numTor):
                tor = self.addStpSwitch(f't{torCount}')
                torSwitches.append(tor)
                torCount += 1
                self.addLink(leaf, tor)

        # Add Hosts and connect to ToRs
        hostCount = 1
        for tor in torSwitches:
            for _ in range(hostsPerTor):
                host = self.addHost(f'h{hostCount}')
                self.addLink(host, tor)
                hostCount += 1
