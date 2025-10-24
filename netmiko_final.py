from netmiko import ConnectHandler
import re


device_ip = ""
username = "admin"
password = "cisco"

# device_params = {
#     "device_type": "cisco_ios",
#     "ip": device_ip,
#     "username": username,
#     "password": password,
#     "conn_timeout": 20,
#     "banner_timeout": 30
# }


def motd():
    print(device_ip)
    device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "conn_timeout": 20,
    "banner_timeout": 30
}
#     status_list = []
    
    with ConnectHandler(**device_params) as ssh:
        
        # result = ssh.send_command("show running-config | include banner motd", use_textfsm=False)
        result = ssh.send_command("show running-config", use_textfsm=False)
        print(result)
        match = re.search(r"banner motd (\S)([\s\S]*?)\1", result, re.DOTALL)
        if match:
            motd_text = match.group(2).strip()
            return motd_text
        else:
            return "Error: No MOTD Configured"
