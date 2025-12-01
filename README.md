# 🔐 Wi-Fi Attack Automation Tool

This tool is a Python-based utility that automates the process of Wi-Fi network penetration testing, including handshake capture, password cracking, DoS attacks, and password list generation. It acts as a wrapper around powerful tools like `aircrack-ng`, `airodump-ng`, `aireplay-ng`, `crunch`, and `wireshark`.

⚠️ **Educational Purposes Only**
This tool is intended for security professionals and researchers on networks they own or are authorized to audit. Unauthorized access or attacks on networks are illegal and unethical.

---

## Project Tree
```
├── assets (All password files created should be in this folder)
│   └── john.lst 
├── LICENSE
├── README.md
├── requirements.txt
├── setup.sh
└── src
    ├── animation.py
    ├── GenCharlist.py
    ├── mac_address_detector.py
    ├── network_scanner.py
    └── wifi_cracker.py
```


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


##  Usage

### 1. Clone the Repository

```bash
git clone https://github.com/cyb2rS2c/Wi-Fi_ATTACK.git
cd Wi-Fi_ATTACK
```

### 2. Run the Tool

```bash
chmod +x setup.sh;./setup.sh
```

Root privileges are required for most network interface operations.

### 3. Follow the Menu

Interactive options guide you through:

```
Welcome to the Attack Menu
1. Find Channel /run it second
2. Capture Handshake
3. Denial of Service (DoS)
4. Crack Handshake
5. Generate Password List (Optional)
6. Restart Network Manager/ ensure this is up before executing 00
00. Find info about AP /run it first
001. See EAPOL in Wireshark
0. Exit
```

---

## ✨ Example Flow

1. Select **00** to list available APs.
2. Select **1** to lock onto a specific channel.
3. Select **2** to capture the handshake.
4. Select **3** to deauth clients and force reconnection.
5. Select **4** to crack the captured handshake.
6. Optionally use **5** to generate a custom wordlist if one is not available.

---

## ✨ Screenshots
<img width="642" height="217" alt="image" src="https://github.com/user-attachments/assets/171f223e-016f-4716-bad8-d110b46bae22" />
<img width="956" height="609" alt="image" src="https://github.com/user-attachments/assets/9248abd5-f035-4726-ac08-8aba8d8b7f00" />



## 🛑 Legal Disclaimer

This software is provided for **educational** and **authorized testing** only. The authors are not responsible for any misuse or damage caused. Always get **explicit permission** before auditing any network.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for more info.

