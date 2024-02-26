from mininet.topo import Topo

class OCS( Topo ):
    def build( self ):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        l1 = self.addLink(h1, h2)