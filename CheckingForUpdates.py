import requests
import json
import os
import sys

GITHUB_RAW_URL = "https://raw.githubusercontent.com/z1ruz-code/IPPulse/main/"
API_RELEASE_URL = "https://api.github.com/repos/z1ruz-code/IPPulse/releases/latest"

def update_file(filename):
    try:
        response = requests.get(GITHUB_RAW_URL + filename)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        return True
    except:
        return False

def check_and_update():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        current_version = config.get("version", "0.0.0")

        response = requests.get(API_RELEASE_URL, timeout=5)
        response.raise_for_status()
        latest_data = response.json()
        latest_version = latest_data.get("tag_name", "").lstrip('v')

        if latest_version and latest_version != current_version:
            choice = input(f"New version available ({latest_version}). Update now? (y/n): ").lower()
            if choice == 'y':
                print("Updating files...")
                files_to_update = ["main.py", "CheckingForUpdates.py"]
                for file in files_to_update:
                    update_file(file)
                
                config["version"] = latest_version
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)
                
                print("Update complete. Restarting...")
                os.execv(sys.executable, ['python'] + sys.argv)
    except:
        pass