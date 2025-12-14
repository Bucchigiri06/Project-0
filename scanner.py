# scanner.py
import socket
import datetime
from database import save_scan

def run_scan(target, ports):
    """
    target: IP or hostname string
    ports: "start-end" string, e.g., "1-1024"
    """
    print(f"Scanning target: {target} on ports: {ports}")

    try:
        start_port, end_port = map(int, ports.split("-"))
    except Exception:
        print("Invalid port format! Use: 1-1024")
        return []

    # Resolve host first
    try:
        ip = socket.gethostbyname(target)
    except Exception as e:
        print(f"Unable to resolve target {target}: {e}")
        return []

    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.35)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"[OPEN] {port}")
                open_ports.append(port)
            sock.close()
        except KeyboardInterrupt:
            print("Scan interrupted by user.")
            break
        except Exception:
            # ignore other exceptions to continue scanning
            continue

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_scan(target, ports, open_ports, timestamp)

    print("\nScan Completed ✓")
    print(f"Open Ports: {open_ports}")
    return open_ports
