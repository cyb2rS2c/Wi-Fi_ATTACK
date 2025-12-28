#!/usr/bin/env bash
set -e

if [[ "$EUID" -ne 0 ]]; then
  exec sudo "$0" "$@"
fi

python3 -m venv testenv; source testenv/bin/activate
pip install Wi-Fi-Attack --upgrade
clear
exec  wifi-cracker 
