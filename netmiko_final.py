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

        
        result = ssh.send_command("show running-config | section banner motd", use_textfsm=True)
        ssh.disconnect()
        if "banner motd" in result:
            match = re.search(r'banner motd \^C\n(.*?)\n\^C', result, re.DOTALL)
            if match:
                motd_text = match.group(1)
                return motd_text
        else:
            return "Error: No MOTD Configured"
