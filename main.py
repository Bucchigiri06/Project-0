# main.py
import sys
from database import init_db
from scanner import run_scan
from gui import launch_gui

def print_usage():
    print("\nUsage:")
    print("  python main.py gui                    - Launch GUI")
    print("  python main.py cli                    - Interactive CLI mode")
    print("  python main.py scan <target> [ports]  - Quick scan")
    print("\nExamples:")
    print("  python main.py gui")
    print("  python main.py cli")
    print("  python main.py scan 192.168.0.101 1-200\n")

def cli_mode():
    print("\n========== CLI Mode ==========\n")
    target = input("Enter Target IP/Domain: ").strip()
    if not target:
        print("Target cannot be empty.")
        return
    ports = input("Enter Port Range (e.g. 1-1000) [default 1-1024]: ").strip()
    if not ports:
        ports = "1-1024"
    run_scan(target, ports)

if __name__ == "__main__":
    init_db()

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    mode = sys.argv[1].lower()
    if mode == "gui":
        launch_gui()
    elif mode == "cli":
        cli_mode()
    elif mode == "scan":
        if len(sys.argv) < 3:
            print("Error: missing target for scan.")
            print_usage()
            sys.exit(1)
        target = sys.argv[2]
        ports = sys.argv[3] if len(sys.argv) >= 4 else "1-1024"
        run_scan(target, ports)
    else:
        print("Unknown command.")
        print_usage()
