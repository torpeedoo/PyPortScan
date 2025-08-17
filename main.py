import argparse
import time
from functions import *

localhost = "127.0.0.1"

def main():

    parser = argparse.ArgumentParser(description="PyPortScan - Lightweight Port Scanner")
    subparsers = parser.add_subparsers(dest='mode', required=True)
    
    # Single port scan
    single_parser = subparsers.add_parser('single', help='Single port scan')
    single_parser.add_argument('ip', help='IP address or hostname to scan')
    single_parser.add_argument('port', type=int, help='Port number to scan')
    single_parser.add_argument('--stealth', action='store_true', help='Enable stealth scanning')
    single_parser.add_argument('--rand_delay', action='store_true', help='Enable random delay between scans')

    # Range port scan
    range_parser = subparsers.add_parser('range', help='Range port scan')
    range_parser.add_argument('ip', help='IP address or hostname to scan')
    range_parser.add_argument('start_port', type=int, help='Start port number')
    range_parser.add_argument('end_port', type=int, help='End port number')
    range_parser.add_argument('--stealth', action='store_true', help='Enable stealth scanning')
    range_parser.add_argument('--rand_delay', action='store_true', help='Enable random delay between scans')

    # List port scan
    list_parser = subparsers.add_parser('list', help='List port scan')
    list_parser.add_argument('ip', help='IP address or hostname to scan')
    list_parser.add_argument('ports', help='Comma-separated list of ports to scan')
    list_parser.add_argument('--stealth', action='store_true', help='Enable stealth scanning')
    list_parser.add_argument('--rand_delay', action='store_true', help='Enable random delay between scans')

    args = parser.parse_args()


    start_time = time.time()
    print(f"\nStarting scan on {args.ip}...\n")

    if args.mode == 'single' and args.stealth:
        scanner1 = Scanner(args.ip)
        result = scanner1.stealth_scan_single_port(args.port)
        if result:
            print(result)

    elif args.mode == 'single':
        scanner1 = Scanner(args.ip)
        result = scanner1.scan_port(args.port)
        if result:
            print(result)


    elif args.mode == 'range' and args.stealth:
        scanner1 = Scanner(args.ip)
        open_ports = scanner1.stealth_scan_ports_range(args.start_port, args.end_port)
        if open_ports:
            print("\nScan complete.")
            print(f"Open ports on {args.ip}: {open_ports}")
        else:
            print(f"Scan complete. No open ports found on {args.ip} in the range {args.start_port}-{args.end_port}.")

    elif args.mode == 'range':
        scanner1 = Scanner(args.ip)
        open_ports = scanner1.scan_ports_range(args.start_port, args.end_port)
        if open_ports:
            print("\nScan complete.")
            print(f"Open ports on {args.ip}: {open_ports}")
        else:
            print(f"Scan complete. No open ports found on {args.ip} in the range {args.start_port}-{args.end_port}.")


    elif args.mode == 'list' and args.stealth:
        port_list = [int(p.strip()) for p in args.ports.split(',')]
        scanner1 = Scanner(args.ip)
        open_ports = scanner1.stealth_scan_ports_list(port_list)
        if open_ports:
            print("\nScan complete.")
            print(f"Open ports on {args.ip}: {open_ports}")
        else:
            print(f"Scan complete. No open ports found on {args.ip} in the provided list.")

    elif args.mode == 'list':
        port_list = [int(p.strip()) for p in args.ports.split(',')]
        scanner1 = Scanner(args.ip)
        open_ports = scanner1.scan_ports_list(port_list)
        if open_ports:
            print("\nScan complete.")
            print(f"Open ports on {args.ip}: {open_ports}")
        else:
            print(f"Scan complete. No open ports found on {args.ip} in the provided list.")

    end_time = time.time()
    print(f"\nTotal scan time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()