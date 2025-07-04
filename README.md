# Keylogger-Implementation
# Educational Keylogger GUI (Python + Tkinter)

 This project is an **educational keylogger demo** built in Python.  
It uses a modern, colorful **Tkinter GUI** to monitor and display system-wide keystrokes in real-time.  
Logged data is timestamped, displayed in a sortable table, and shows session stats like total keys, session start time, and last key pressed.

 **Important:**  
This tool is for **authorized educational or demonstration use only**.  
Logging keystrokes on machines without explicit permission is **illegal and unethical**.  
Always use responsibly within a test environment.

---

## Features

 **System-wide keylogging on Windows**  
- Captures all keystrokes globally, including special keys like `[Enter]`, `[Space]`, `[Backspace]`.

 **Rich real-time GUI**  
- Built with Tkinter + ttk for a modern look.
- Blinking status indicator (green when active, red when inactive).
- Warning bar to emphasize ethical use.

**Live session statistics**  
- Displays total keys pressed, session start time, and the last key captured.

 **Interactive table log**  
- Shows `Timestamp`, `Key`, and `Key Name`.
- Scrollable `Treeview` with clean styling.

**User controls**  
-  Start Logging
-  Stop Logging
-  Clear Log (resets counters and log)

 **Thread-safe & responsive**  
- Uses `pynput` for background listening.
- GUI updates via `after()` keep the interface smooth.

---

## Installation

### Requirements

- **Python 3.7+** (tested on Python 3.10 & 3.11)
- Packages:
pip install pynput
