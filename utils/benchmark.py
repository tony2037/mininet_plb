import subprocess
import re

def pingAllTest(net):
    net.pingAll()

def parse_port_stats(output):
    # Parse the output bytes object and extract port statistics into a dictionary
    stats = {}
    # Parse the lines and remove header: OFPST_PORT reply
    lines = output.decode().split('ports\n')[1]
    lines = re.sub(r'\n\s*tx pkts', ', tx pkts', lines)
    lines = lines.split('\n')[0:-1]
    for line in lines:
        #print(line)
        #print("------")
        if 'port LOCAL' in line: # Skip loopback port
            continue
        port_name = line.split(':')[0].strip()
        port_stats = {}
        key_values = line[line.find("tx pkts"):].split(',')
        #print(port_name,": ", key_values, sep="")
        for key_value in key_values:
            key, value = key_value.split("=")
            port_stats[key.strip()] = int(value)
        stats[port_name] = port_stats
    return stats

def calculate_load_imbalance(stats):
    if not stats:
        return None

    # Store transmitted bytes for each port
    tx_bytes = []
    
    # Extract received bytes for each port from the parsed statistics
    for port_stats in stats.values():
        # Ensure 'bytes' key is present in port statistics
        if 'bytes' in port_stats:
            tx_bytes.append(port_stats['bytes'])

    # Check if no statistics were extracted
    if not tx_bytes:
        return None

    # Calculate load imbalance
    max_utilization = max(tx_bytes)
    min_utilization = min(tx_bytes)
    load_imbalance = max_utilization - min_utilization

    # Calculate total received bytes across all ports
    total_tx_bytes = sum(tx_bytes)

    # Calculate load imbalance percentage
    load_imbalance_percentage = (load_imbalance / total_tx_bytes) * 100
    return "{:.3f}%".format(load_imbalance_percentage)

def load_imbalance_test(net):

    # Get switches list(a: aggregation block, s: spine block, t: top of rack)
    switches = net.switches
    #print("a: aggregation block, s: spine block, t: top of rack")
    # Gather port statistics
    for switch in switches:
        print(switch.name)
        output = subprocess.check_output(['ovs-ofctl', 'dump-ports', switch.name])
        #print(output)
        stats = parse_port_stats(output)
        print(stats)
        li = calculate_load_imbalance(stats)
        print("Load Imbalance (LI):", li)
        
#TESTS = [pingAllTest]
TESTS = [load_imbalance_test]
