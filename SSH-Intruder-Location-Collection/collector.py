import csv
import os
import time
import requests

INPUT_FILE = "banned_ips.txt"
OUTPUT_FILE = "attackers.csv"
API_URL = "http://ip-api.com/json/{}"
RATE_LIMIT_DELAY = 1  # seconds

FIELDS = [
    "ip", "country", "region", "city",
    "isp", "org", "asn", "lat", "lon"
]


def load_existing_ips(csv_file):
    """Load already-enriched IPs from CSV."""
    existing_ips = set()

    if os.path.exists(csv_file):
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ips.add(row["ip"])

    return existing_ips


def load_banned_ips(input_file):
    """Load banned IPs from Fail2Ban output file."""
    with open(input_file) as f:
        return {line.strip() for line in f if line.strip()}


def enrich_ip(ip):
    """Query IP intelligence provider."""
    try:
        response = requests.get(API_URL.format(ip), timeout=5)
        data = response.json()

        if data.get("status") != "success":
            return None

        return {
            "ip": ip,
            "country": data.get("country"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "asn": data.get("as"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }

    except Exception as e:
        print(f"[!] Error enriching {ip}: {e}")
        return None


def main():
    banned_ips = load_banned_ips(INPUT_FILE)
    existing_ips = load_existing_ips(OUTPUT_FILE)

    new_ips = banned_ips - existing_ips

    if not new_ips:
        print("[+] No new IPs to enrich.")
        return

    file_exists = os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        for ip in new_ips:
            print(f"[+] Enriching {ip}")
            result = enrich_ip(ip)

            if result:
                writer.writerow(result)

            time.sleep(RATE_LIMIT_DELAY)

    print(f"[✓] Enrichment complete. New IPs added: {len(new_ips)}")


if __name__ == "__main__":
    main()
