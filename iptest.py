import subprocess
from concurrent.futures import ThreadPoolExecutor
import requests
import json

def get_country_code(ip_address):
    """Gets the country code for an IP address using an external API."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data.get("status") == "success":
            return data.get("countryCode")
        else:
            return "Unknown"
    except requests.exceptions.RequestException as e:
        print(f"Error getting country code for {ip_address}: {e}")
        return "Unknown"
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {ip_address}: {e}")
        return "Unknown"

def process_ip(ip_address):
    curl_command = f'curl --resolve www.cloudflare.com:443:{ip_address} https://www.cloudflare.com:443/cdn-cgi/trace -s --connect-timeout 3 --max-time 5'
    result = subprocess.run(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_dict = {}
    if result.stdout:
        country_code = get_country_code(ip_address)
        with open('proxyip.txt', 'a') as outfile:
            outfile.write(f'{ip_address}#{country_code}\n')  # Add country code to output
        pairs = result.stdout.split("\n")
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result_dict[key.strip()] = value.strip()
    else:
        print(f"no proxy {ip_address}")

# Read IP addresses from file
with open('ip.txt', 'r') as file:
    ip_addresses = file.read().splitlines()

# Process IP addresses with multithreading
with ThreadPoolExecutor(max_workers=128) as executor:
    executor.map(process_ip, ip_addresses)
