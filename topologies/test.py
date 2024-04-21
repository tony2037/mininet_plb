from mininet.topo import Topo
from mininet.link import TCLink, TCIntf, Link

class Test(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.server = self.addHost('server', bw=10)
        self.s1 = self.addSwitch('s1', bw=5)
        self.s2 = self.addSwitch('s2', bw=5)
        self.addLink(self.s1, self.s2, bw=10, delay='10ms', loss=0, max_queue_size=10, use_htb=True)
        self.addLink(self.s1, self.server, bw=10, delay='10ms', loss=0, max_queue_size=10, use_htb=True)
        self.addLink(self.s2, self.server, bw=10, delay='10ms', loss=0, max_queue_size=10, use_htb=True)

        self.clients = []
        for i in range(5):
            c = self.addHost(f'client{i}', bw=10)
            self.addLink(c, self.s1, bw=10, delay='10ms', loss=0, max_queue_size=10, use_htb=True)
            self.clients.append(c)

        
# Topology to be instantiated in Mininet
class StarTopo(Topo):
    "Star topology for Buffer Sizing experiment"

    def __init__(self, n=3, cpu=None, bw_host=10, bw_net=5,
                 delay='10ms', maxq=2, enable_dctcp=True, enable_red=True,
                 show_mininet_commands=False, red_params=None):
        # Add default members to class.
        super(StarTopo, self ).__init__()
        self.n = n
        self.cpu = cpu
        self.bw_host = bw_host
        self.bw_net = bw_net
        self.delay = delay
        self.maxq = maxq
        self.enable_dctcp = enable_dctcp
        self.enable_red = enable_red
        self.red_params = red_params
        self.show_mininet_commands = show_mininet_commands;
        
        print("enable dctcp: %d" % self.enable_dctcp)
        print("enable red: %d" % self.enable_red)
        
        self.create_topology()

    # Create the experiment topology 
    # Set appropriate values for bandwidth, delay, 
    # and queue size 
    def create_topology(self):
        # Host and link configuration
        hconfig = {'cpu': self.cpu}

        if self.enable_dctcp:
            print("Enabling ECN for senders/receiver...")
        
        lconfig_sender = {'bw': self.bw_host, 'delay': self.delay,
                          'max_queue_size': self.maxq,
                          'show_commands': self.show_mininet_commands}
        lconfig_receiver = {'bw': self.bw_net, 'delay': 0,
                            'max_queue_size': self.maxq,
                            'show_commands': self.show_mininet_commands}                            
        lconfig_switch = {'bw': self.bw_net, 'delay': 0,
                            'max_queue_size': self.maxq,
                            'enable_ecn': 1 if self.enable_dctcp else 0,
                            'enable_red': 1 if self.enable_red else 0,
                            'red_params': self.red_params if ( (self.enable_red or self.enable_dctcp) and self.red_params != None) else None,
                            'show_commands': self.show_mininet_commands}                            
        
        n = self.n
        
        # Create the receiver
        receiver = self.addHost('receiver')

        # Create the (sole) switch
        switch = self.addSwitch('s0')

        # Create the sender hosts
        hosts = []
        for i in range(n-1):
            hosts.append(self.addHost('h%d' % (i+1), **hconfig))

        # Interface numbers
        host_to_switch, switch_to_receiver, receiver_to_switch = 1, 0, 2
        
        # Hook the receiver up to the switch
        self.addLink(receiver, switch, cls=Link,
                      port1=receiver_to_switch, port2=switch_to_receiver,
                      cls1=TCIntf, cls2=TCIntf,
                      params1=lconfig_receiver, params2=lconfig_switch)
#                      params1={'bw':10}, params2={'bw':10})

        # Create links between hosts and switch
        for i in range(n-1):
            self.addLink(hosts[i], switch,
                port1=host_to_switch, port2=i+1, **lconfig_sender)
