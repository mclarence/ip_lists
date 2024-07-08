import requests
from IPy import IP

def extract_ips(data):
    if isinstance(data, dict):
        for key, value in data.items():
            extract_ips(value)
    elif isinstance(data, list):
        for item in data:
            extract_ips(item)
    elif isinstance(data, str):  # Basic check to identify IP address strings
        try:
            IP(data, ipversion=4)
            ip_addresses.append(data)
        except ValueError:
            pass


external_lists = [
    {
        "name": "okta",
        "url": "https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json",
    },
    {
        "name": "google",
        "url": "https://www.gstatic.com/ipranges/goog.json",
    }
]


for external_list in external_lists:
    try:
        ip_addresses = []
        response = requests.get(external_list["url"])

        if response.status_code == 200:
            if external_list['url'].endswith(".json"):
                data = response.json()
                extract_ips(data)
            else:
                raise ValueError("Unsupported file format")
        else:
            raise ValueError("Failed to fetch data")
    except Exception as e:
        print(f"Failed to fetch data from {external_list['name']}: {e}")
        continue

    with open(f"{external_list['name']}.txt", "w") as f:
        for ip in ip_addresses:
            f.write(f"{ip}\n")

    print(f'Extracted {len(ip_addresses)} IP addresses from {external_list["name"]}')

        