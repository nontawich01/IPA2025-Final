from ncclient import manager
import xmltodict

ip = ""

m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

if_name = "Loopback66070276"

def check_interface(if_name):
    filter_xml = f"""
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{if_name}</name>
            </interface>
        </interfaces>
    </filter>
    """
    resp = m.get_config(source="running", filter=filter_xml)
    data = xmltodict.parse(resp.xml)
    interfaces = data.get("rpc-reply", {}).get("data", {}).get("interfaces", {}).get("interface")
    if interfaces:
        return True
    return False

def create():
    if check_interface(if_name):
            return "Cannot create: Interface loopback 66070276"
    else:
        netconf_config = """
        <config>
              <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                  <name>{if_name}</name>
                  <description>Created by NETCONF</description>
                  <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                  </type>
                  <enabled>true</enabled>
                  <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                      <ip>172.2.76.1</ip>
                      <netmask>255.255.255.0</netmask>
                    </address>
                  </ipv4>
                </interface>
              </interfaces>
            </config>
    """
        try:
            netconf_reply = netconf_edit_config(netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 66070276 is created successfully using Netconf"
        except:
            print("Error!")


def delete():
    if not check_interface(if_name):
            return "Cannot delete: Interface loopback 66070276"
    else:
        netconf_config = """
        <config>
              <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                  <name>{if_name}</name>
                </interface>
              </interfaces>
            </config>
        """

        try:
            netconf_reply = netconf_edit_config(netconf_config)
            xml_data = netconf_reply.xml
            print(xml_data)
            if '<ok/>' in xml_data:
                return "Interface loopback 66070276 is deleted successfully using Netconf"
        except:
            print("Error!")


# def enable():
#     netconf_config = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         netconf_reply = netconf_edit_config(netconf_config)
#         xml_data = netconf_reply.xml
#         print(xml_data)
#         if '<ok/>' in xml_data:
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#         print("Error!")


# def disable():
#     netconf_config = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         netconf_reply = netconf_edit_config(netconf_config)
#         xml_data = netconf_reply.xml
#         print(xml_data)
#         if '<ok/>' in xml_data:
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#         print("Error!")

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)


# def status():
#     netconf_filter = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         # Use Netconf operational operation to get interfaces-state information
#         netconf_reply = m.<!!!REPLACEME with the proper Netconf operation!!!>(filter=<!!!REPLACEME with netconf_filter!!!>)
#         print(netconf_reply)
#         netconf_reply_dict = xmltodict.<!!!REPLACEME with the proper method!!!>(netconf_reply.xml)

#         # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
#         if <!!!REPLACEME with the proper condition!!!>:
#             # extract admin_status and oper_status from netconf_reply_dict
#             admin_status = <!!!REPLACEME!!!>
#             oper_status = <!!!REPLACEME !!!>
#             if admin_status == 'up' and oper_status == 'up':
#                 return "<!!!REPLACEME with proper message!!!>"
#             elif admin_status == 'down' and oper_status == 'down':
#                 return "<!!!REPLACEME with proper message!!!>"
#         else: # no operation-state data
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#        print("Error!")
