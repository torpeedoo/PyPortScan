import socket
from scapy.all import IP, TCP, sr1

def scan_port(port, ip):

    # Try to interpret ip as an IP address; if it fails, resolve as hostname
    try:
        socket.inet_aton(ip)
        # Valid IP address
    except socket.error:
        # Not a valid IP, try to resolve as hostname
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            print(f"Could not resolve {ip}")
            return False
    
    #scan the specified port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            return f"Port {port} is open on {ip}" if result == 0 else f"Port {port} is closed on {ip}"
    except socket.error as e:
        print(f"Socket error: {e}")
        return False
    
def scan_ports_range(start_port, end_port, ip, timeout=0.1):

    open_ports = []

    # Try to interpret ip as an IP address; if it fails, resolve as hostname
    try:
        socket.inet_aton(ip)
        # Valid IP address
    except socket.error:
        # Not a valid IP, try to resolve as hostname
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            print(f"Could not resolve {ip}")
            return False
    
    #scan the specified ports
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"Port {port} is open on {ip}")
                else:
                    print(f"Port {port} is closed on {ip}")
        except socket.error as e:
            print(f"Socket error: {e}")
    
    return open_ports if open_ports else None

def scan_ports_list(port_list, ip, timeout=0.1):

    open_ports = []

    # Try to interpret ip as an IP address; if it fails, resolve as hostname
    try:
        socket.inet_aton(ip)
        # Valid IP address
    except socket.error:
        # Not a valid IP, try to resolve as hostname
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            print(f"Could not resolve {ip}")
            return False
    
    #scan the specified ports
    for port in port_list:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"Port {port} is open on {ip}")
                else:
                    print(f"Port {port} is closed on {ip}")
        except socket.error as e:
            print(f"Socket error: {e}")
    
    return open_ports if open_ports else None

def stealth_scan_single_port(port, ip, timeout=0.1):

    # Try to interpret ip as an IP address; if it fails, resolve as hostname
    try:
        socket.inet_aton(ip)
        # Valid IP address
    except socket.error:
        # Not a valid IP, try to resolve as hostname
        try:
            ip = socket.gethostbyname(ip)
        except socket.gaierror:
            print(f"Could not resolve {ip}")
            return False
    
    # Send SYN packet
    syn_packet = IP(dst=ip)/TCP(dport=port, flags='S')
    response = sr1(syn_packet, timeout=timeout, verbose=0)
    if response is None:
        return f"Port {port} is filtered or host is down on {ip}"
    if response.haslayer(TCP):
        if response[TCP].flags == 0x12:  # SYN-ACK
            # Send RST to close the connection (do not complete handshake)
            rst_packet = IP(dst=ip)/TCP(dport=port, flags='R', seq=response[TCP].ack)
            sr1(rst_packet, timeout=timeout, verbose=0)
            return f"Port {port} is open on {ip} (stealth scan)"
        elif response[TCP].flags == 0x14:  # RST-ACK
            return f"Port {port} is closed on {ip} (stealth scan)"
    return f"Port {port} is filtered or host is down on {ip} (stealth scan)"

def stealth_scan_ports_range(start_port, end_port, ip, timeout=0.1):
    #ssend SYN packets for each port in the range
    open_ports = []
    for port in range(start_port, end_port + 1):
        result = stealth_scan_single_port(port, ip, timeout)
        if "open" in result:
            open_ports.append(port)
            print(result)
        else:
            print(result)
    return open_ports if open_ports else None

def stealth_scan_ports_list(port_list, ip, timeout=0.1):
    open_ports = []
    for port in port_list:
        result = stealth_scan_single_port(port, ip, timeout)
        if "open" in result:
            open_ports.append(port)
            print(result)
        else:
            print(result)
    return open_ports if open_ports else None