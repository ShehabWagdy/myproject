import tkinter as tk
from tkinter import messagebox
from netmiko import Netmiko
import traceback

# List of device IPs (you can add more devices here)
device_ips = [
    '192.168.1.10',
    '192.168.1.11',
    '192.168.1.12',
    '192.168.1.13'

    # Add more device IPs as needed
]

def configure_subnet():
    # Get the values from the entry fields
    subnet = subnet_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    for index, ip in enumerate(device_ips, start=1):
        device_params = {
            'device_type': 'cisco_nxos',
            'ip': ip,
            'username': username,
            'password': password,
            'read_timeout_override': 120,
            'session_log': f'session_log_device_{index}.txt'
        }
        # Configuration commands
        commands_to_configure = [
            f'ip prefix-list test-6 permit {subnet}',
        ]
        save_configurations = 'copy running-config startup-config'
        try:
            net_connect = Netmiko(**device_params)
            output = net_connect.send_config_set(commands_to_configure)
            save_config = net_connect.send_command(save_configurations)
            net_connect.disconnect()
        except Exception as e:
            # Show error message
            messagebox.showerror("Error", f"An error occurred on device {index} ({device_params['ip']}): {e}")
            print(traceback.format_exc())
            return
    # Show success message
    messagebox.showinfo("Success", "Configuration commands applied successfully on all devices.")
# Create the main window
root = tk.Tk()
root.title("Subnet Configuration")
# Create and place the subnet label and entry field
subnet_label = tk.Label(root, text="Enter the subnet to be configured:")
subnet_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
subnet_entry = tk.Entry(root)
subnet_entry.grid(row=0, column=1, padx=10, pady=5)
# Create and place the username label and entry field
username_label = tk.Label(root, text="Enter your username:")
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)
# Create and place the password label and entry field
password_label = tk.Label(root, text="Enter your password:")
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)
# Create and place the configure button
configure_button = tk.Button(root, text="Configure Subnet", command=configure_subnet)
configure_button.grid(row=3, column=0, columnspan=2, pady=10)
# Run the main loop
root.mainloop()