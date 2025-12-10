# Wi-Fi Attack Automation Tool
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/%7C%20Linux-green?logo=linux)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Version](https://img.shields.io/badge/Version-2.0-orange)

---
This tool is a Python-based utility that automates the process of Wi-Fi network penetration testing, including handshake capture, password cracking, DoS attacks, and password list generation. It acts as a wrapper around powerful tools like `aircrack-ng`, `airodump-ng`, `aireplay-ng`, `crunch`, and `wireshark`.

**For Authorized Penetration Testing Only**
This tool is intended for security professionals and researchers on networks they own or are authorized to audit. Unauthorized access or attacks on networks are illegal and unethical.

---

## Features

* Scan for Access Points and capture detailed information.
* Detect and lock on target network channels.
* Capture WPA/WPA2 handshakes.
* Launch deauthentication (DoS) attacks.
* Crack captured handshakes using a wordlist or custom-generated passwords.
* Generate password lists with custom masks using `crunch`.
* Launch Wireshark for EAPOL packet inspection.
* Interactive terminal-based menu interface.

---


## Project Tree
```
├── assets (All password files created should be in this folder)
│   ├── generated_password.txt
│   └── john.lst
├── LICENSE
├── README.md
├── requirements.txt
├── setup.sh
└── src
    ├── animation.py
    ├── GenCharlist.py
    ├── Get_AP.py
    ├── mac_address_detector.py
    ├── network_scanner.py
    └── wifi_cracker.py
```

##  Usage

### 1. Clone the Repository

```bash
git clone https://github.com/cyb2rS2c/Wi-Fi_ATTACK.git
cd Wi-Fi_ATTACK
```

## 2. Run 

```bash
chmod +x setup.sh;source ./setup.sh
```
Root privileges are required for most network interface operations.

## Screenshots
<img width="642" height="217" alt="image" src="https://github.com/user-attachments/assets/171f223e-016f-4716-bad8-d110b46bae22" />
<img width="956" height="609" alt="image" src="https://github.com/user-attachments/assets/9248abd5-f035-4726-ac08-8aba8d8b7f00" />
<img width="399" height="193" alt="image2" src="https://github.com/user-attachments/assets/4a1133a9-cd2e-4aaa-9e9f-6b751624cf37" />


## Legal Disclaimer

This software is provided for **educational** and **authorized testing** only. The authors are not responsible for any misuse or damage caused. Always get **explicit permission** before auditing any network.

---

## License

MIT License. See [LICENSE](LICENSE) for more info.

