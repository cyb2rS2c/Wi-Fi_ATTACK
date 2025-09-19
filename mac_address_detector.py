import subprocess
import sys
import re
import pyfiglet
from termcolor import colored
import time
import os

def animated_print(text, delay=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_text(text, color="red"):
    os.system("clear")  # or "cls" on Windows
    figlet = pyfiglet.Figlet(font='slant')
    ascii_art = figlet.renderText(text)
    colored_art = colored(ascii_art, color)

    # Animate the ASCII banner character by character
    animated_print(colored_art, delay=0.0005)

    # Animate the copyright
    copy_right = colored("By cyb2rS2c", 'blue')
    animated_print(copy_right, delay=0.01)


# Function to scan the network with Nmap
def scan_network(ip_range):
    result = subprocess.run(['nmap', '-sS', ip_range], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode()

# Function to parse the Nmap output for IP, MAC, and State
def find_mac_and_state(scan_output):
    # Regex pattern for matching IP, MAC address, and state
    ip_mac_pattern = r"(\d+\.\d+\.\d+\.\d+)\s+(Host is up|Host is down).*?MAC Address:\s([0-9A-Fa-f:]{17})\s*\((.*?)\)"
    host_pattern = r"(\d+\.\d+\.\d+\.\d+)\s+(Host is up|Host is down)"

    mac_data = {}
    
    # Capture IP, MAC, state, and device type for devices with MAC addresses
    for match in re.finditer(ip_mac_pattern, scan_output, re.DOTALL):
        ip = match.group(1)
        state = match.group(2)
        mac = match.group(3)
        device_type = match.group(4)
        mac_data[ip] = (mac, state, device_type)
    
    # Capture IP and state for devices with no MAC address listed (only "Host is up" or "Host is down")
    for match in re.finditer(host_pattern, scan_output):
        ip = match.group(1)
        state = match.group(2)
        
        # Only add IP if not already added (avoid duplicates)
        if ip not in mac_data:
            mac_data[ip] = ("N/A", state, "Unknown")
    
    return mac_data

# Function to display help message
def show_help():
    help_message = """
    MAC Address Detector - Scan your network for devices based on IP range and MAC address.

    Usage:
      python3 mac_address_detector.py <ip_range> <mac_address> [--only]

    Options:
      <ip_range>       : The IP range to scan (e.g., 192.168.0.1-20 or 192.168.0.0/24).
      <mac_address>    : The MAC address to search for (optional).
      --only           : Optionally, display only the device with the matching MAC address.
      --help           : Show this help message.

    Example 1: Scan a range and display all results
      python3 mac_address_detector.py 192.168.1.1-20

    Example 2: Scan a range and search for a specific MAC address
      python3 mac_address_detector.py 192.168.1.1-20 XX:XX:XX:XX:XX:XX

    Example 3: Scan a range and only display the matching MAC address (if found)
      python3 mac_address_detector.py 192.168.1.1-20 XX:XX:XX:XX:XX:XX --only

    Author: cyb2rS2c
    """
    print(help_message)


# Main script
if __name__ == "__main__":
    # If --help is provided, display help message and exit
    if "--help" in sys.argv:
        show_help()
        sys.exit(0)

    # Check if correct number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python3 mac_checker.py <ip_range> <mac_address> [--only]")
        sys.exit(1)

    ip_range = sys.argv[1].strip()
    
    mac_address = None
    if len(sys.argv) > 2:
        mac_address = sys.argv[2].strip()

    print_text("MAC address Detector")

    # Scan the network
    scan_output = scan_network(ip_range)

    # Parse the scan output to extract IP, MAC, state, and device type
    mac_data = find_mac_and_state(scan_output)

    found = False
    # If a MAC address is provided, only show the matching result
    if mac_address:
        for ip, (mac, state, device_type) in mac_data.items():
            if mac.lower() == mac_address.lower():
                # Color the state based on whether it is "up" or "down"
                color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
                print(f"{ip:<20}{mac:<20}{color_state:<20}{device_type}")
                found = True
                break  # Break once the specific MAC address is found

    # If no MAC address is provided or no match was found, display everything
    if not mac_address or not found:
        print(f"{'IP Address':<20}{'MAC Address':<20}{'State':<20}{'Device Type'}")
        print("-" * 70)
        for ip, (mac, state, device_type) in mac_data.items():
            # Color the state based on whether it is "up" or "down"
            color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
            print(f"{ip:<20}{mac:<20}{color_state:<20}{device_type}")

    if mac_address and not found:
        print(f"MAC Address {mac_address} is NOT detected in the network scan.")

    print("Scan completed!")
