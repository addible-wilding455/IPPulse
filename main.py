import requests
import json
import time
import os
import CheckingForUpdates

CheckingForUpdates.check_and_update()

ip_address = input("Enter IP address: ")
url = f"https://api.ipapi.is/?q={ip_address}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "company" in data:
        data["company"].pop("whois", None)
    if "asn" in data:
        data["asn"].pop("whois", None)

    json_output = json.dumps(data, indent=4)
    
    for line in json_output.splitlines():
        print(line)
        time.sleep(0.01)

    save_choice = input("\nSave result to .txt? (y/n): ").lower()
    if save_choice == 'y':
        folder = "reports"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.abspath(os.path.join(folder, f"{ip_address}.txt"))
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(json_output)
        print(f"Saved: {filepath}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")