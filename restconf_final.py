import json
import requests
requests.packages.urllib3.disable_warnings()

router_ip = ""

api_base = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")

def check_interface(if_name):
    url = f"{api_base}/interface={if_name}?fields=name"
    resp = requests.get(url, auth=basicauth, headers=headers, verify=False, timeout=10)
    if resp.status_code == 200:
        return True 
    elif resp.status_code == 404:
        return False
    

