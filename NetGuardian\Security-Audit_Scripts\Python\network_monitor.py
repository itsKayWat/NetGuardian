import subprocess
import socket
import time
import sys
import re
import os
import ctypes
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
from threading import Thread
import traceback
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with admin rights"""
    try:
        if not is_admin():
            # Get the path to the Python interpreter
            python_exe = sys.executable
            # Get the path to this script
            script = os.path.abspath(sys.argv[0])
            # Re-run with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, script, None, 1)
            sys.exit()
    except Exception as e:
        print(f"Error elevating privileges: {e}")
        return False
    return True

class NetworkMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Protection Monitor")
        self.root.geometry("800x600")
        
        # Prevent accidental closure
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Add minimize to tray button
        self.minimize_button = tk.Button(self.root, text="Minimize to Tray", command=self.minimize_to_tray)
        self.minimize_button.pack(pady=5)
        
        # Add status label
        self.status_label = tk.Label(self.root, text="Status: Monitoring", fg="green")
        self.status_label.pack(pady=5)
        
        # Add text area with scrollbar
        self.log_area = scrolledtext.ScrolledText(self.root, width=80, height=30)
        self.log_area.pack(padx=10, pady=10)
        
        # Add clear button
        self.clear_button = tk.Button(self.root, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(pady=5)

        # Add exit button
        self.exit_button = tk.Button(self.root, text="Exit Monitor", command=self.on_closing)
        self.exit_button.pack(pady=5)

        # Initialize monitoring thread
        self.monitoring = True
        self.monitor_thread = Thread(target=self.monitor_network, daemon=True)

    # ... [previous methods remain the same] ...

    def start(self):
        # Start monitoring thread
        self.monitor_thread.start()
        
        # Show startup message
        messagebox.showinfo("Monitor Started", 
            "Network Protection Monitor is now running.\n\n" +
            "- The window can be minimized\n" +
            "- Monitoring will continue in background\n" +
            "- Alerts will appear in the log\n\n" +
            "Click OK to continue.")
        
        # Start GUI
        self.root.mainloop()

if __name__ == "__main__":
    try:
        # Try to elevate privileges if needed
        if not is_admin():
            run_as_admin()
        else:
            app = NetworkMonitorGUI()
            app.start()
    except Exception as e:
        # If we can't show GUI error, fall back to console
        print(f"Critical error: {str(e)}\n{traceback.format_exc()}")
        input("Press Enter to exit...")