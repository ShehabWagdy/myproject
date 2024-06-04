import csv
from netmiko import ConnectHandler

 
# Define the CSV headers and the output file path

csv_header = ["Host Name", "IP", "Serial Number"]

output_file_path = "add the path for the new csv sheet file"

 
# Read devices from the input CSV file

with open("csv sheet file name") as file:

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

 

            # Print serial number and hostname for verification

            #print(f"Serial Number: {serial_number}")

            #print(f"Hostname: {hostname}")

 

            # Append the results to the list

            results.append({

                "Host Name": hostname,

                "IP": device['host'],

                "Serial Number": serial_number

            })

 

        except Exception as e:

            # Handle exceptions and print an error message

            #print(f"Failed to connect to {device['host']}: {e}")

 

# Write the results to the output CSV file

with open(output_file_path, mode="w", newline="") as f:

    writer = csv.DictWriter(f, fieldnames=csv_header)

    # Write the header

    writer.writeheader()

    # Write the rows of data

    writer.writerows(results)

 

#print(f"Output saved to {output_file_path}")

 
