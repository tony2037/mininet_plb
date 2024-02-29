from mininet.topo import Topo
from mininet.node import OVSBridge
from .base import Base

class OCS( Base ):
    #def __init__( self, nAggr=4, nToR=16, nSrv=15 ):
    def __init__( self, nAggr=2, nToR=2, nSrv=3 ):
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

        for i in range(len(self.aggrBlocks)):
            for j in range(i+1, len(self.aggrBlocks)):
                self.addLink(self.aggrBlocks[i], self.aggrBlocks[j])
