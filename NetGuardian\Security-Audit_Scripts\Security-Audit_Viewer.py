import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from datetime import datetime
from ttkthemes import ThemedTk

class SystemFileViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("System File Viewer")
        self.root.geometry("1400x800")
        
        # Set dark theme
        self.configure_dark_theme()
        
        # Data structure to store computer information
        self.computers = {}
        
        # Create main layout
        self.create_layout()
        
        # Load saved data if exists
        self.load_saved_data()

    def configure_dark_theme(self):
        # Configure dark theme colors
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'select_bg': '#404040',
            'select_fg': '#ffffff',
            'button_bg': '#404040',
            'button_fg': '#ffffff',
            'text_bg': '#1e1e1e',
            'text_fg': '#ffffff'
        }
        
        style = ttk.Style()
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TButton', background=self.colors['button_bg'], foreground=self.colors['button_fg'])
        style.configure('Dark.TNotebook', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TNotebook.Tab', background=self.colors['button_bg'], foreground=self.colors['fg'])
        
        self.root.configure(bg=self.colors['bg'])

    def create_layout(self):
        # Create main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create left panel for computer list
        left_panel = ttk.Frame(main_container, style='Dark.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Computer list
        ttk.Label(left_panel, text="Computers", style='Dark.TLabel').pack(pady=5)
        self.computer_listbox = tk.Listbox(left_panel, width=30, 
                                         bg=self.colors['text_bg'],
                                         fg=self.colors['text_fg'],
                                         selectbackground=self.colors['select_bg'],
                                         selectforeground=self.colors['select_fg'])
        self.computer_listbox.pack(fill=tk.Y, expand=True)
        self.computer_listbox.bind('<<ListboxSelect>>', self.on_select_computer)
        
        # Buttons
        ttk.Button(left_panel, text="Add Computer", command=self.add_computer, style='Dark.TButton').pack(pady=5, fill=tk.X)
        ttk.Button(left_panel, text="Load Directory", command=self.load_directory, style='Dark.TButton').pack(pady=5, fill=tk.X)
        ttk.Button(left_panel, text="Remove Computer", command=self.remove_computer, style='Dark.TButton').pack(pady=5, fill=tk.X)
        
        # Create right panel for file viewing
        right_panel = ttk.Frame(main_container, style='Dark.TFrame')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(right_panel, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.tabs = {
            "CMD History": ttk.Frame(self.notebook, style='Dark.TFrame'),
            "Network Processes": ttk.Frame(self.notebook, style='Dark.TFrame'),
            "Recent Files": ttk.Frame(self.notebook, style='Dark.TFrame'),
            "Network Connections": ttk.Frame(self.notebook, style='Dark.TFrame'),
            "Running Processes": ttk.Frame(self.notebook, style='Dark.TFrame')
        }
        
        # Add tabs to notebook
        for name, tab in self.tabs.items():
            self.notebook.add(tab, text=name)
            text = tk.Text(tab, wrap=tk.NONE,
                         bg=self.colors['text_bg'],
                         fg=self.colors['text_fg'],
                         insertbackground=self.colors['fg'])
            scrolly = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=text.yview)
            scrollx = ttk.Scrollbar(tab, orient=tk.HORIZONTAL, command=text.xview)
            text.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
            
            scrolly.pack(side=tk.RIGHT, fill=tk.Y)
            scrollx.pack(side=tk.BOTTOM, fill=tk.X)
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def load_directory(self):
        directory = filedialog.askdirectory(title="Select Directory Containing System Files")
        if directory:
            # Get computer name from directory name
            computer_name = os.path.basename(directory)
            if not computer_name:  # If directory ends with separator
                computer_name = os.path.basename(os.path.dirname(directory))
            
            # File mappings
            file_mappings = {
                "cmd_history": "cmd_history.txt",
                "network_processes": "network_processes.txt",
                "recent_files": "recent_files.txt",
                "network_connections": "network_connections.txt",
                "running_processes": "running_processes.txt"
            }
            
            # Initialize computer data
            self.computers[computer_name] = {}
            
            # Load each file if it exists
            for key, filename in file_mappings.items():
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.computers[computer_name][key] = f.read()
                except FileNotFoundError:
                    self.computers[computer_name][key] = f"File not found: {filename}"
                except Exception as e:
                    self.computers[computer_name][key] = f"Error loading {filename}: {str(e)}"
            
            # Update computer list
            if computer_name not in self.computer_listbox.get(0, tk.END):
                self.computer_listbox.insert(tk.END, computer_name)
            
            # Save data
            self.save_data()
            
            # Display the data
            self.computer_listbox.selection_clear(0, tk.END)
            index = self.computer_listbox.get(0, tk.END).index(computer_name)
            self.computer_listbox.selection_set(index)
            self.display_computer_data(computer_name)
            
            messagebox.showinfo("Success", f"Loaded data for {computer_name}")

    def add_computer(self):
        computer_name = tk.simpledialog.askstring("Add Computer", "Enter computer name:",
                                                parent=self.root)
        if computer_name:
            if computer_name in self.computers:
                messagebox.showerror("Error", "Computer already exists!")
                return
                
            self.computers[computer_name] = {
                "cmd_history": "",
                "network_processes": "",
                "recent_files": "",
                "network_connections": "",
                "running_processes": ""
            }
            
            self.computer_listbox.insert(tk.END, computer_name)
            self.load_files_for_computer(computer_name)
            self.save_data()

    def remove_computer(self):
        selection = self.computer_listbox.curselection()
        if selection:
            computer_name = self.computer_listbox.get(selection)
            if messagebox.askyesno("Confirm", f"Remove {computer_name}?"):
                del self.computers[computer_name]
                self.computer_listbox.delete(selection)
                self.clear_tabs()
                self.save_data()

    def load_files_for_computer(self, computer_name):
        # File mappings
        file_mappings = {
            "cmd_history": "cmd_history.txt",
            "network_processes": "network_processes.txt",
            "recent_files": "recent_files.txt",
            "network_connections": "network_connections.txt",
            "running_processes": "running_processes.txt"
        }
        
        # Create directory for computer if it doesn't exist
        computer_dir = os.path.join("computer_data", computer_name)
        if not os.path.exists(computer_dir):
            os.makedirs(computer_dir)
        
        # Load each file
        for key, filename in file_mappings.items():
            filepath = filedialog.askopenfilename(
                title=f"Select {filename} for {computer_name}",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filepath:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.computers[computer_name][key] = f.read()
                
                # Copy file to computer's directory
                with open(os.path.join(computer_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(self.computers[computer_name][key])

    def on_select_computer(self, event):
        selection = self.computer_listbox.curselection()
        if selection:
            computer_name = self.computer_listbox.get(selection)
            self.display_computer_data(computer_name)

    def display_computer_data(self, computer_name):
        if computer_name not in self.computers:
            return
            
        data = self.computers[computer_name]
        
        # Map data to tabs
        tab_mapping = {
            "CMD History": "cmd_history",
            "Network Processes": "network_processes",
            "Recent Files": "recent_files",
            "Network Connections": "network_connections",
            "Running Processes": "running_processes"
        }
        
        # Update each tab
        for tab_name, data_key in tab_mapping.items():
            text_widget = self.tabs[tab_name].winfo_children()[0]  # Get text widget
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, data[data_key])

    def clear_tabs(self):
        for tab in self.tabs.values():
            text_widget = tab.winfo_children()[0]  # Get text widget
            text_widget.delete(1.0, tk.END)

    def save_data(self):
        if not os.path.exists("computer_data"):
            os.makedirs("computer_data")
            
        data = {
            "last_updated": datetime.now().isoformat(),
            "computers": self.computers
        }
        
        with open("computer_data/viewer_data.json", 'w') as f:
            json.dump(data, f, indent=4)

    def load_saved_data(self):
        try:
            with open("computer_data/viewer_data.json", 'r') as f:
                data = json.load(f)
                self.computers = data["computers"]
                
                # Update computer list
                for computer_name in self.computers:
                    self.computer_listbox.insert(tk.END, computer_name)
                    
        except FileNotFoundError:
            pass

def main():
    root = ThemedTk(theme="black")
    app = SystemFileViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()