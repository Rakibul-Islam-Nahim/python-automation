# SSH-Intruder Location Collection

## Overview

This project is a **real-world SOC-style threat intelligence collector** that extracts attacker IPs banned by **Fail2Ban**, enriches them with **geolocation and ISP intelligence**, and stores the results in a structured CSV file for analysis.

Unlike simulated labs, this project uses **real attacker data** from a public VPS, demonstrating how SOC analysts collect, enrich, and analyze hostile IP activity in production environments.

---

## Objectives

- Collect real attacker IPs blocked by Fail2Ban
- Enrich IPs with geographic and network metadata
- Avoid duplicate enrichment to save API usage
- Automate the workflow using Bash + Python
- Store results in an analyst-friendly format (CSV)

---

## SOC Skills Demonstrated

- Log analysis (Fail2Ban)
- Threat intelligence enrichment
- Automation & scripting (Bash + Python)
- Data normalization and deduplication
- Defensive security mindset
- Working with real-world attack telemetry

---

## Project Structure

SSH-Intruder-Location-Collection  
├── attackers.csv  
├── banned_ips.txt  
├── collector.py  
├── README.md  
└── run_Collector.sh

---

## Workflow

![Architecture-Diagram](/SSH-Intruder-Location-Collection/diagrams/Architecture-Diagram.drawio.png)

1. **Fail2Ban** detects and bans malicious SSH login attempts
2. Bash script extracts banned IPs from `/var/log/fail2ban.log`
3. Python script:
   - Loads existing enriched IPs
   - Queries IP intelligence only for new IPs
   - Appends enriched data to `attackers.csv`
4. Dataset is ready for analysis or visualization

---

## Data Collected

For each attacker IP:

- IP Address
- Country
- Region
- City
- ISP
- Organization
- ASN
- Latitude / Longitude

---

## Tools Used

- Linux Based Cloud VPS
- Python 3.10.12
- Python libraries: `requests` , `csvkit`

**Usage**: `sudo run_collector.sh`

---

## Sample Output:

[`Attacker CSV data`](/SSH-Intruder-Location-Collection/resources/attackers.md)

| ip              | country         | region         | city              | isp                                     | org                                     | asn                                             | lat     | lon      |
| --------------- | --------------- | -------------- | ----------------- | --------------------------------------- | --------------------------------------- | ----------------------------------------------- | ------- | -------- |
| 94.26.106.109   | Germany         | Hesse          | Kriftel           | SAS GENIUSWEER                          |                                         | AS215607 dataforest GmbH                        | 50.084… | 8.472…   |
| 68.183.218.89   | Germany         | Hesse          | Frankfurt am Main | DigitalOcean, LLC                       | DigitalOcean, LLC                       | AS14061 DigitalOcean, LLC                       | 50.117… | 8.684…   |
| 106.227.90.101  | China           | Jiangxi        | Taohua            | China Telecom                           | Chinanet JX                             | AS149837 China Telecom                          | 28.674… | 115.910… |
| 146.190.22.211  | The Netherlands | North Holland  | Amsterdam         | DigitalOcean, LLC                       | DigitalOcean, LLC                       | AS14061 DigitalOcean, LLC                       | 52.352… | 4.939…   |
| 117.162.140.162 | China           | Beijing        | Jinrongjie        | China Mobile communications corporation | China Mobile                            | AS56045 China Mobile communications corporation | 39.916… | 116.360… |
| 218.205.31.101  | China           | Jiangsu        | Nanjing           | China Mobile communications corporation | China Mobile Communications Corporation | AS56046 China Mobile communications corporation | 32.061… | 118.763… |
| 159.223.51.11   | Singapore       | South West     | Singapore         | DigitalOcean, LLC                       | DigitalOcean, LLC                       | AS14061 DigitalOcean, LLC                       | 1.321…  | 103.695… |
| 161.35.145.74   | The Netherlands | North Holland  | Amsterdam         | DigitalOcean, LLC                       | DigitalOcean, LLC                       | AS14061 DigitalOcean, LLC                       | 52.352… | 4.939…   |
| 45.140.17.124   | Russia          | St.-Petersburg | St Petersburg     | Proton66 OOO                            | Proton66 LLC                            | AS198953 Proton66 OOO                           | 59.942… | 30.310…  |

---

## My Purpose:

Due to limited system resources on my low-end device, continuously monitoring logs using full SIEM solutions (such as Wazuh) can be time-consuming and inefficient. This automation provides a faster response by quickly capturing important details about intruder activity, making the process more reliable and lightweight for my environment.

Additionally, the stored `attackers.csv` dataset will be useful for future projects, including machine learning experiments. For this repository, the `attackers.csv` file will not be updated further.

---

## Proof Of Concept:

| Fail2Ban's Ban list                                                   | Fail2Ban Logs                                                    | Script Collect Recent Ban                                            |
| --------------------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- |
| ![](/SSH-Intruder-Location-Collection/screenshots/banListUpdated.png) | ![](/SSH-Intruder-Location-Collection/screenshots/logStatus.png) | ![](/SSH-Intruder-Location-Collection/screenshots/newServedJail.png) |

**Result**: As shown above, a new intruder IP (80.94.92.164) was successfully banned by **Fail2Ban**, and its details were successfully collected and enriched by the **script**, along with the corresponding timestamp.

---

## Author:

_**Rakib Ul Islam Nahim**_    
Cybersecurity / SOC Analyst Enthusiast    
I am focusing on practical learning while fully utilizing my available resources

---

## ⚠️ Disclaimer

This project is for educational and defensive security purposes only.
All collected data comes from automated attack activity against a controlled VPS environment.

_(End of Showcase)_
