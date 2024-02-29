from mininet.topo import Topo
from mininet.node import OVSBridge

class Base( Topo ):
    def __init__( self ):
        Topo.__init__(self)

    def addStpSwitch( self, name ):
        switchOpts = {'cls': OVSBridge,'stp': 1}
        sw = self.addSwitch(name, **switchOpts)
        return sw

    def test( self ):
        print('Defaut testsuite: pingall')