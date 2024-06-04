# Network Device Serial Number Retriever
This repository contains a Python script that retrieves serial numbers from network devices using Netmiko. The script reads device information from an input CSV file, connects to each device, retrieves the serial number, and writes the results to an output CSV file.

## Overview
The script performs the following steps:

Reads device information (hostnames, IP addresses, etc.) from an input CSV file.
Connects to each device using SSH.
Executes a command to retrieve the serial number.
Saves the hostname, IP address, and serial number of each device to an output CSV file.

## Prerequisites
Python 3.x
netmiko library

## Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/network-device-serial-number-retriever.git
cd network-device-serial-number-retriever
```
2. Install the required Python libraries:
```
pip install netmiko
```
## Usage
1. Prepare the input CSV file (serial_number.csv) with the following headers:

- `device_type`: The type of device (e.g., cisco_ios).
- `host`: The IP address or hostname of the device.
- `username`: The SSH username.
- `password`: The SSH password.
- `secret`: The enable password (if required).

Example of `serial_number.csv`:
```
device_type,host,username,password,secret(if enabled)
cisco_ios,192.168.1.1,admin,password,secret(if enabled)
cisco_ios,192.168.1.2,admin,password,secret(if enabled)
```
2. Update the script with the correct paths for the input and output CSV files:
```
input_file_path = "serial_number.csv"
output_file_path = "serial_number.csv"
```
3. Run the script:
```
python retrieve_serial_numbers.py
```
4. The output CSV file (`out_serial_number.csv`) will be generated with the following headers:
- `Host Name`: The hostname of the device.
-`IP`: The IP address of the device.
-`Serial Number`: The serial number of the device.

## Script Details
```
import csv
from netmiko import ConnectHandler

# Define the CSV headers and the output file path
csv_header = ["Host Name", "IP", "Serial Number"]
output_file_path = "out_serial_number.csv"

# Read devices from the input CSV file
with open("serial_number.csv") as file:
    devices = csv.DictReader(file)
    results = []

    # Loop through each device in the CSV
    for device in devices:
        try:
            # Establish connection to the device
            connection = ConnectHandler(**device)
            print(f"Connecting to IP: {device['host']}")

            # Send command to retrieve the serial number
            output = connection.send_command("show version | include Processor board ID")
            # Extract the serial number from the output
            serial_number = output.split("Processor board ID")[-1].strip()
            # Get the hostname of the device
            hostname = connection.find_prompt()[:-1]
            # Disconnect from the device
            connection.disconnect()

            # Append the results to the list
            results.append({
                "Host Name": hostname,
                "IP": device['host'],
                "Serial Number": serial_number
            })

        except Exception as e:
            print(f"Failed to connect to {device['host']}: {e}")

# Write the results to the output CSV file
with open(output_file_path, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_header)
    # Write the header
    writer.writeheader()
    # Write the rows of data
    writer.writerows(results)

print(f"Output saved to {output_file_path}")
```
## Contributing
If you have any suggestions or improvements, feel free to open an issue or submit a pull request. Contributions are welcome!

## Contact
For any questions or inquiries, please contact https://www.linkedin.com/in/shehabwagdy 
