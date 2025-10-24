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
    
def create():
    if_name = "Loopback66070276"

    if check_interface(if_name):
        return "Cannot create: Interface loopback 66070276"
    
    else:
        yangConfig = {
            "ietf-interfaces:interface": {
                "name": "Loopback66070276",
                "description": "Created by RESTCONF",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {"ip": "172.2.76.1", "netmask": "255.255.255.0"}
                    ]
                },
                "ietf-ip:ipv6": {}
            }
        }
        api_url = f"{api_base}/interface={if_name}"
        resp = requests.put(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )
        if 200 <= resp.status_code <= 299:
            return "Interface loopback 66070276 is created successfully using Restconf"
    