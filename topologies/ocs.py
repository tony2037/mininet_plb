from mininet.topo import Topo
from mininet.node import OVSBridge
from mininet.link import TCLink
from .base import Base

class OCS( Base ):
    #def __init__( self, nAggr=4, nToR=16, nSrv=15 ):
    def __init__( self, nAggr=8, nToR=1, nSrv=1 ):
        self.aggrBlocks = []
        self.ToRs = []
        self.Servers = []
        Base.__init__(self)

        for index in range(nAggr):
            aggrName = f'A{index}'
            aggrBlock = self.addStpSwitch(aggrName)
            self.aggrBlocks.append(aggrBlock)
            for tor in range(nToR):
                ToRName = f'{aggrName}_T{tor}'
                ToR = self.addStpSwitch(ToRName)
                self.ToRs.append(ToR)
                self.addLink(ToR, aggrBlock)
                for srv in range(nSrv):
                    srvName = f'{ToRName}_h{srv}'
                    server = self.addHost(srvName)
                    self.Servers.append(server)
                    self.addLink(server, ToR)

        self.addLink(self.aggrBlocks[0], self.aggrBlocks[7], cls=TCLink, bw=5)
        for i in range(0, 7):
            self.addLink(self.aggrBlocks[i], self.aggrBlocks[i+1], cls=TCLink, bw=2)
