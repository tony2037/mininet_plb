def pingAllTest(net):
    net.pingAll()

def tcpCongestion(net):
    server = net['server']
    server_ip = server.IP()
    clients = []
    for i in range(5):
        clients.append(net[f'client{i}'])
    s1 = net['s1']
    s2 = net['s2']
    server.popen(['iperf', '-s', '-w', '16m'])
    for client in clients:
        client.popen(f'iperf -c {server_ip} -i 1 -w 16m -M 1460 -N -Z cubic -t 30')
    s1.popen('tcpdump > tcpdump.txt')
    s2.popen('tcpdump > tcpdump.txt')

TESTS = [tcpCongestion]
