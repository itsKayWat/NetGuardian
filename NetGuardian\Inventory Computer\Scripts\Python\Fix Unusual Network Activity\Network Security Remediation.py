import psutil
import socket
import subprocess
import os
import sys
import time
import logging
from datetime import datetime
from threading import Thread, Lock
from collections import defaultdict
import win32serviceutil
import win32service
import win32event
import servicemanager

class NetworkMonitor:
    def __init__(self):
        try:
            # Initialize basic components first
            self.running = True
            self.lock = Lock()
            self.blocked_ips = set()
            self.threat_scores = defaultdict(int)
            self.connection_history = defaultdict(list)
            
            # Setup logging before anything else
            self.setup_logging()
            
            # Load configurations
            self.whitelist = self.load_whitelist()
            
            self.logger.info("NetworkMonitor initialized successfully")
            
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            sys.exit(1)

    def setup_logging(self):
        """Configure logging with error handling"""
        try:
            # Create logs directory in a common location
            log_dir = os.path.join(os.path.expanduser('~'), 'NetworkMonitor', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # Setup main logger
            self.logger = logging.getLogger('NetworkSecurity')
            self.logger.setLevel(logging.INFO)
            
            # Create log file with timestamp
            log_file = os.path.join(log_dir, f'network_security_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            handler = logging.FileHandler(log_file)
            
            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(handler)
            
            # Add console handler for immediate feedback
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Logging setup failed: {str(e)}")
            raise

    def load_whitelist(self):
        """Load whitelisted processes and IPs"""
        try:
            whitelist = {
                'processes': {
                    'chrome.exe',
                    'msedge.exe',
                    'firefox.exe',
                    'svchost.exe',
                    'MpDefenderCoreService.exe',
                    'SearchApp.exe',
                    'smartscreen.exe',
                    'System'
                },
                'ips': {
                    '13.64.180.106',
                    '51.116.253.169',
                    '20.69.137.228',
                    '127.0.0.1',
                    '192.168.0.1',
                    '192.168.1.1'
                }
            }
            return whitelist
            
        except Exception as e:
            self.logger.error(f"Failed to load whitelist: {str(e)}")
            return {'processes': set(), 'ips': set()}

    def handle_suspicious_connection(self, process_name, pid, remote_ip, remote_port):
        """Handle suspicious connections safely"""
        try:
            # Check whitelist first
            if process_name in self.whitelist['processes'] or remote_ip in self.whitelist['ips']:
                return False
            
            # Log suspicious connection
            log_msg = (f"SUSPICIOUS: Connection from {process_name} "
                      f"(PID: {pid}) to {remote_ip}:{remote_port}")
            self.logger.warning(log_msg)
            
            with self.lock:
                if remote_ip not in self.blocked_ips:
                    try:
                        # Add firewall rule
                        rule_name = f"Blocked_IP_{remote_ip}".replace('.', '_')
                        subprocess.run([
                            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                            f'name="{rule_name}"',
                            'dir=out',
                            'action=block',
                            f'remoteip={remote_ip}'
                        ], capture_output=True, text=True, check=True)
                        
                        self.blocked_ips.add(remote_ip)
                        self.logger.info(f"Successfully blocked IP: {remote_ip}")
                        
                    except subprocess.CalledProcessError as e:
                        self.logger.error(f"Failed to add firewall rule: {str(e)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error handling suspicious connection: {str(e)}")
            return False

    def monitor_connections(self):
        """Main monitoring loop with error handling"""
        self.logger.info("Starting connection monitoring...")
        
        while self.running:
            try:
                connections = psutil.net_connections(kind='inet')
                
                for conn in connections:
                    if not self.running:
                        break
                        
                    if conn.status == 'ESTABLISHED' and conn.raddr:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                            remote_ip = conn.raddr.ip
                            remote_port = conn.raddr.port
                            
                            self.handle_suspicious_connection(
                                process_name,
                                conn.pid,
                                remote_ip,
                                remote_port
                            )
                            
                        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                            self.logger.debug(f"Process access error: {str(e)}")
                            continue
                
                time.sleep(1)  # Prevent high CPU usage
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
                time.sleep(5)  # Back off on error

    def stop(self):
        """Safely stop the monitor"""
        self.running = False
        self.logger.info("Stopping network monitor...")

def main():
    try:
        monitor = NetworkMonitor()
        monitor.monitor_connections()
    except KeyboardInterrupt:
        print("\nShutting down...")
        monitor.stop()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()