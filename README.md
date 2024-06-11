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
  ```
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
     @python3 /home/myk410/show_ip_gui.py
     ```

5. **Reboot the Raspberry Pi:**

   Reboot your Raspberry Pi to test if the script runs at startup:

   ```bash
   sudo reboot
   ```

When the Raspberry Pi boots up and the desktop environment loads, the script should run and display the IP address in a pop-up window using Tkinter.



If the script isn't running on startup, you can try using `crontab` to schedule the script to run at boot time. Here’s how you can do it:

1. **Open the Crontab Editor:**

   ```bash
   crontab -e
   ```

2. **Add the Script to Crontab:**

   Add the following line to the crontab file to run the script at boot:

   ```bash
   @reboot DISPLAY=:0 python3 /home/myk410/show_ip_gui.py
   ```

   Replace `/path/to/your/show_ip_gui.py` with the actual path to your Python script. The `DISPLAY=:0` part ensures that the script runs with the display environment, which is necessary for GUI applications.

3. **Save and Exit:**

   Save the changes and exit the editor. If you're using `nano`, you can do this by pressing `CTRL + X`, then `Y`, and then `Enter`.

4. **Reboot the Raspberry Pi:**

   Reboot your Raspberry Pi to test if the script runs at startup:

   ```bash
   sudo reboot
   ```

### Troubleshooting

If it still doesn't work, there are a few things you can check:

- **Check Crontab Logs:**
  - You can check the logs to see if there are any errors. Use the following command to view the cron logs:
    ```bash
    grep CRON /var/log/syslog
    ```

- **Verify Script Path:**
  - Ensure the path to the Python script is correct in the crontab entry.

- **Check Script Permissions:**
  - Make sure the script is executable:
    ```bash
    chmod +x /home/myk410/show_ip_gui.py
    ```

If everything is set up correctly, the script should run at startup and display the IP address in a pop-up window on the desktop.
