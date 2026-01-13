#!/bin/bash


WORKDIR="/opt/fail2ban-collector"   # change if needed
LOGFILE="/var/log/fail2ban.log"
INPUT_FILE="banned_ips.txt"
SCRIPT="collector.py"

echo "[+] Starting Fail2Ban collection..."

# Ensure script is run as root (fail2ban log needs it)
if [[ $EUID -ne 0 ]]; then
    echo "[!] Please run as root"
    exit 1
fi

cd "$WORKDIR" || {
    echo "[!] Cannot access $WORKDIR"
    exit 1
}

# Step 1: Extract banned IPs
echo "[+] Extracting banned IPs from Fail2Ban logs..."
grep " Ban " "$LOGFILE" | awk '{print $NF}' | sort -u > "$INPUT_FILE"

if [[ ! -s "$INPUT_FILE" ]]; then
    echo "[!] No banned IPs found."
    exit 0
fi

echo "[+] Found $(wc -l < "$INPUT_FILE") unique banned IPs"

# Step 2: Run Python collector
echo "[+] Running Python enrichment script..."
python3 "$SCRIPT"

echo "[✓] Collection and enrichment completed."
