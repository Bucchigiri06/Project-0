# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import socket
import datetime
import re

from database import save_scan   # ✅ IMPORTANT


def launch_gui():
    root = tk.Tk()
    root.title("Zenmap — Network Mapper")
    root.geometry("950x620")
    root.configure(bg="#0b1220")
    root.resizable(False, False)

    # ================= STYLES =================
    style = ttk.Style()
    style.theme_use("default")

    style.configure("TLabel", background="#0b1220", foreground="#e5e7eb", font=("Consolas", 10))
    style.configure("TButton", font=("Consolas", 10), padding=6)
    style.configure("TEntry", fieldbackground="#020617", foreground="#e5e7eb", padding=6)
    style.configure("Treeview", font=("Consolas", 10), rowheight=24)
    style.configure("Treeview.Heading", font=("Consolas", 10, "bold"))

    # ================= HEADER =================
    ttk.Label(
        root,
        text="Zenmap — Network Mapper",
        font=("Consolas", 18, "bold"),
        foreground="#38bdf8"
    ).pack(pady=10)

    # ================= CONTROL PANEL =================
    control_panel = ttk.Frame(root, padding=12)
    control_panel.pack(fill="x", padx=20)

    card = ttk.Frame(control_panel, padding=14)
    card.pack(anchor="center")

    ttk.Label(card, text="Target:", font=("Consolas", 11, "bold")).grid(row=0, column=0, padx=6, pady=6)
    target_entry = ttk.Entry(card, width=35)
    target_entry.grid(row=0, column=1, padx=6, pady=6)

    scan_btn = ttk.Button(card, text="Scan", width=12)
    scan_btn.grid(row=0, column=2, padx=12)

    ttk.Label(card, text="Command:", font=("Consolas", 11, "bold")).grid(row=1, column=0, padx=6, pady=6)
    command_entry = ttk.Entry(card, width=60)
    command_entry.insert(0, "nmap -p 1-1024")
    command_entry.grid(row=1, column=1, columnspan=2, padx=6, pady=6)

    # ================= NOTEBOOK =================
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=15, pady=10)

    # Nmap Output
    output_tab = ttk.Frame(notebook)
    notebook.add(output_tab, text="Nmap Output")
    output_text = tk.Text(output_tab, bg="#020617", fg="#22c55e",
                          font=("Consolas", 10), insertbackground="white")
    output_text.pack(fill="both", expand=True)

    # Ports / Hosts
    ports_tab = ttk.Frame(notebook)
    notebook.add(ports_tab, text="Ports / Hosts")
    ports_table = ttk.Treeview(ports_tab, columns=("port", "state", "service"), show="headings")
    ports_table.heading("port", text="Port")
    ports_table.heading("state", text="State")
    ports_table.heading("service", text="Service")
    ports_table.pack(fill="both", expand=True)

    # Host Details
    host_tab = ttk.Frame(notebook)
    notebook.add(host_tab, text="Host Details")
    host_info = tk.Text(host_tab, bg="#020617", fg="#e5e7eb", font=("Consolas", 10))
    host_info.pack(fill="both", expand=True)

    # ================= SCAN LOGIC =================
    def run_scan():
        target = target_entry.get().strip()
        base_cmd = command_entry.get().strip()

        if not target:
            messagebox.showerror("Error", "Target is required")
            return

        output_text.delete("1.0", "end")
        ports_table.delete(*ports_table.get_children())
        host_info.delete("1.0", "end")

        cmd = base_cmd.split() + [target]
        output_text.insert("end", f"$ {' '.join(cmd)}\n\n")

        start_time = datetime.datetime.now()
        open_ports = []

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                output_text.insert("end", line)
                output_text.see("end")

                match = re.match(r"(\d+)/tcp\s+open\s+(\S+)", line)
                if match:
                    port, service = match.groups()
                    open_ports.append(port)
                    ports_table.insert("", "end", values=(port, "open", service))

            end_time = datetime.datetime.now()
            ip = socket.gethostbyname(target)

            host_info.insert("end", f"Host: {target}\n")
            host_info.insert("end", f"IP Address: {ip}\n")
            host_info.insert("end", f"Scan Started: {start_time}\n")
            host_info.insert("end", f"Scan Finished: {end_time}\n\n")
            host_info.insert("end", "Open Ports:\n")

            for p in open_ports:
                host_info.insert("end", f"  - Port {p}\n")

            # ================= SAVE TO DATABASE ✅ =================
            timestamp = end_time.strftime("%Y-%m-%d %H:%M:%S")
            save_scan(target, base_cmd, open_ports, timestamp)

        except FileNotFoundError:
            messagebox.showerror("Nmap Not Found", "Nmap is not installed or not in PATH.")

    scan_btn.config(command=lambda: threading.Thread(target=run_scan, daemon=True).start())
    root.mainloop()
