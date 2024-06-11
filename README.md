To display the IP address in a pop-up window on the Raspberry Pi's desktop at startup, you can use the `tkinter` library in Python for creating the pop-up window. Follow these steps:

1. **Install Tkinter:**
   Tkinter is usually pre-installed on Raspbian, but you can install it if it's not available:

   ```bash
   sudo apt-get install python3-tk
   ```

2. **Write the Python Script:**

   Create a new Python script, for example, `show_ip_gui.py`, with the following content:

   ```python
import socket
import fcntl
import struct
import tkinter as tk
from tkinter import messagebox

def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24])
        return ip_address
    except IOError:
        return None

def show_ip():
    eth_ip = get_ip_address('eth0')
    wlan_ip = get_ip_address('wlan0')

    if eth_ip:
        messagebox.showinfo("IP Address", f"Ethernet IP Address: {eth_ip}")
    elif wlan_ip:
        messagebox.showinfo("IP Address", f"Wi-Fi IP Address: {wlan_ip}")
    else:
        messagebox.showerror("Error", "Could not get IP address.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    show_ip()
    root.mainloop()
   ```

   This script uses `tkinter` to create a message box that displays the IP address.

3. **Make the Script Executable:**

   Change the permissions of the script to make it executable:

   ```bash
   chmod +x show_ip_gui.py
   ```

4. **Set Up the Script to Run at Startup:**

   To run the script at startup and display the pop-up on the desktop, you can use the `autostart` feature of the LXDE desktop environment.

   - Create a new autostart file or edit the existing one:

     ```bash
     sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
     ```

   - Add the following line to the end of the file:

     ```bash
     @python3 /path/to/your/show_ip_gui.py
     ```

     Replace `/path/to/your/show_ip_gui.py` with the actual path to your Python script.

5. **Reboot the Raspberry Pi:**

   Reboot your Raspberry Pi to test if the script runs at startup:

   ```bash
   sudo reboot
   ```

When the Raspberry Pi boots up and the desktop environment loads, the script should run and display the IP address in a pop-up window using Tkinter.
