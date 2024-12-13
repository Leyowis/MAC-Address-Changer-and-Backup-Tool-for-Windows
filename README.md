# MAC Address Changer and Backup Tool for Windows

This Python script allows you to easily change the MAC addresses of your network adapters on Windows. It also includes functionality to back up your current MAC addresses, ensuring you can restore them if needed.

## Features:
- List all available network adapters.
- Change the MAC address of any selected adapter (you can either input a custom MAC address or generate a random one).
- Backup current MAC addresses to a text file.

## Prerequisites:
- Python 3.x
- Administrator privileges (to change MAC addresses)

## Usage:
1. Clone or download the repository.
2. Run the script as an administrator to change the MAC address of a network adapter.
3. The script will list all enabled/connected network adapters and ask you to choose one for modification.
4. You can either input a new MAC address or choose to generate a random one.
5. The script will back up the current MAC addresses to a file (`mac_backup.txt`).
