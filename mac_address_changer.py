import subprocess
import re
import random

# Define a regex to validate MAC address format
mac_address_regex = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

# Function to generate a random MAC address
def generate_random_mac():
    mac = [random.choice("02468ACE") + random.choice("0123456789ABCDEF")]
    mac += ["{:02X}".format(random.randint(0, 255)) for _ in range(5)]
    return "-".join(mac)

# Function to list available network adapters
def list_network_adapters():
    adapters = []
    output = subprocess.run(["netsh", "interface", "show", "interface"], capture_output=True, text=True).stdout
    for line in output.splitlines():
        if "Enabled" in line or "Connected" in line:
            parts = line.split()
            adapters.append(parts[-1])  # Adapter name
    return adapters

# Function to backup the current MAC addresses to a file
def backup_mac_addresses(adapters, backup_file="mac_backup.txt"):
    try:
        with open(backup_file, "w") as file:
            for adapter in adapters:
                output = subprocess.run(["getmac", "/v", "/fo", "list"], capture_output=True, text=True).stdout
                for line in output.splitlines():
                    if adapter in line:
                        mac_line = next((l for l in output.splitlines() if "Physical Address" in l), None)
                        if mac_line:
                            mac_address = mac_line.split(":")[-1].strip()
                            file.write(f"{adapter}: {mac_address}\n")
                            break
        print(f"MAC addresses successfully backed up to {backup_file}.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

# Function to change the MAC address of an adapter
def change_mac_address(adapter_name, new_mac):
    if not mac_address_regex.match(new_mac):
        print("Invalid MAC address format! Please enter a valid address.")
        return

    # Commands to change the MAC address
    disable_cmd = ["netsh", "interface", "set", "interface", adapter_name, "admin=disable"]
    enable_cmd = ["netsh", "interface", "set", "interface", adapter_name, "admin=enable"]
    set_mac_cmd = ["netsh", "interface", "set", "interface", adapter_name, "newmac=" + new_mac]

    try:
        subprocess.run(disable_cmd, check=True)
        subprocess.run(set_mac_cmd, check=True)
        subprocess.run(enable_cmd, check=True)
        print(f"MAC address for {adapter_name} successfully changed to {new_mac}.")
    except subprocess.CalledProcessError:
        print("Failed to change the MAC address. Try running the script as an administrator.")

# User selects the adapter and provides the new MAC address
adapters = list_network_adapters()
if not adapters:
    print("No network adapters found.")
else:
    print("Available Network Adapters:")
    for idx, adapter in enumerate(adapters):
        print(f"{idx}: {adapter}")

    # Backup operation
    backup_mac_addresses(adapters)

    adapter_index = int(input("Select the number of the adapter whose MAC address you want to change: "))
    if 0 <= adapter_index < len(adapters):
        use_random = input("Would you like to use a random MAC address? (Y/n): ").lower()
        if use_random == "y":
            new_mac = generate_random_mac()
            print(f"Randomly generated MAC address: {new_mac}")
        else:
            new_mac = input("Enter the new MAC address (e.g., 00-11-22-33-44-55): ")
        change_mac_address(adapters[adapter_index], new_mac)
    else:
        print("Invalid adapter selection.")
