import socket
from scapy.all import IP, TCP, sr1
import random
import time

class Scanner:
    def __init__(self, ip, timeout=0.1):
        self.timeout = timeout
        self.ip = self.resolve_ip(ip)
        if not self.ip:
            raise ValueError(f"Could not resolve {ip}")

    def get_local_subnet(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't have to be reachable
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        # Extract subnet (first three octets)
        subnet = '.'.join(local_ip.split('.')[:3])
        return subnet

    def wait_random_delay(self, max_delay=1.0):
        delay = random.uniform(0.1, max_delay)
        time.sleep(delay)
        print(f"Waiting for {delay:.2f} seconds before next scan...")

    def resolve_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return ip  # already a valid IP
        except socket.error:
            try:
                return socket.gethostbyname(ip)  # resolve hostname
            except socket.gaierror:
                return None
            
    def local_host_discovery(self, ports_list, delay=False, max_delay=1.0):
        hosts_up = {}
        
        subnet = self.get_local_subnet()
        print(f"Local subnet detected: {subnet}.0/24")

        for ip in range(1, 255):
            host = f"{subnet}.{ip}"
            self.ip = host  # Update the scanner's IP for each host
            print(f"Scanning {host}...")
            try:
                ports = self.scan_ports_list(ports_list, delay, max_delay)
                #print(f"{host} is reachable!")
                if ports: hosts_up[host] = ports
            except Exception as e:
                print(e)
            
            if delay:
                self.wait_random_delay(max_delay)

        return hosts_up if hosts_up else None

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.ip, port))
                status = "open" if result == 0 else "closed"
                print(f"Port {port} is {status} on {self.ip}")
                return status == "open"
        except socket.error as e:
            print(f"Socket error: {e}")
            return False

    def scan_ports_range(self, start_port, end_port, delay=False, max_delay=1.0):
        open_ports = []
        for port in range(start_port, end_port + 1):
            if self.scan_port(port):
                open_ports.append(port)

            if delay: self.wait_random_delay(max_delay)
        return open_ports if open_ports else None

    def scan_ports_list(self, port_list, delay=False, max_delay=1.0):
        open_ports = []
        for port in port_list:
            if self.scan_port(port):
                open_ports.append(port)

            if delay: self.wait_random_delay(max_delay)
        return open_ports if open_ports else None

    def stealth_scan_port(self, port):
        syn_packet = IP(dst=self.ip)/TCP(dport=port, flags='S')
        response = sr1(syn_packet, timeout=self.timeout, verbose=0)
        if response is None:
            result = f"Port {port} is filtered or host is down on {self.ip}"
        elif response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK
                rst_packet = IP(dst=self.ip)/TCP(dport=port, flags='R', seq=response[TCP].ack)
                sr1(rst_packet, timeout=self.timeout, verbose=0)
                result = f"Port {port} is open on {self.ip} (stealth scan)"
            elif response[TCP].flags == 0x14:  # RST-ACK
                result = f"Port {port} is closed on {self.ip} (stealth scan)"
            else:
                result = f"Port {port} is filtered or host is down on {self.ip} (stealth scan)"
        print(result)
        return "open" in result

    def stealth_scan_ports_range(self, start_port, end_port, delay=False, max_delay=1.0):
        open_ports = []
        for port in range(start_port, end_port + 1):
            if self.stealth_scan_port(port):
                open_ports.append(port)
            
            if delay: self.wait_random_delay(max_delay)
        return open_ports if open_ports else None

    def stealth_scan_ports_list(self, port_list, delay=False, max_delay=1.0):
        open_ports = []
        for port in port_list:
            if self.stealth_scan_port(port):
                open_ports.append(port)
            
            if delay: self.wait_random_delay(max_delay)
        return open_ports if open_ports else None