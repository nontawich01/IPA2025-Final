from ncclient import manager
import xmltodict

ip = ""

# m = manager.connect(
#     host=ip,
#     port=830,
#     username="admin",
#     password="cisco",
#     hostkey_verify=False
#     )

if_name = "Loopback66070276"

def check_interface(if_name):
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
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
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    if check_interface(if_name):
            return "Cannot create: Interface loopback 66070276"
    else:
        netconf_config = f"""
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
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    if not check_interface(if_name):
            return "Cannot delete: Interface loopback 66070276"
    else:
        netconf_config = f"""
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


def enable():
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    if not check_interface(if_name):
            return "Cannot enable: Interface loopback 66070276 (checked by Netconf)"
    netconf_config = f"""
    <config>
          <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>{if_name}</name>
              <enabled>true</enabled>
            </interface>
          </interfaces>
        </config>        
    """
    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070276 is enabled successfully using Netconf"
    except:
        print("Error!")


def disable():
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    if not check_interface(if_name):
            return "Cannot disable: Interface loopback 66070276 (checked by Netconf)"
    netconf_config = f"""
    <config>
          <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>{if_name}</name>
              <enabled>false</enabled>
            </interface>
          </interfaces>
        </config>          
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070276 is disabled successfully using Netconf"
    except:
        print("Error!")

def netconf_edit_config(netconf_config):
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    return  m.edit_config(target="running", config=netconf_config)


def status():
    m = manager.connect(
    host=ip,
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )
    if not check_interface(if_name):
        return "No Interface loopback 66070276 (checked by Netconf)"
    netconf_filter = f"""
    <filter>
          <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <name>{if_name}</name>
            </interface>
          </interfaces-state>
        </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        iface = netconf_reply_dict.get("rpc-reply").get("data").get("interfaces-state").get("interface")
        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if iface:
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = iface.get("admin-status")
            oper_status = iface.get("oper-status")
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070276 is enabled (checked by Restconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070276 is disabled (checked by Restconf)"
        else: # no operation-state data
            return f"No operational data for interface {if_name}"
    except:
       print("Error!")
