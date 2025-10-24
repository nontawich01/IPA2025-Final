#######################################################################################
# Yourname:
# Your student ID:
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests
import json
import time
import os
import restconf_final
import netconf_final
import ansible_final
import netmiko_final
import re

from requests_toolbelt.multipart.encoder import MultipartEncoder

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")
ROOM_ID =os.environ.get("ROOM_ID")
#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    ROOM_ID
)
ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
method = ""
responseMessage = ""

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    getHTTPHeader = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    message = messages[0]["text"]
    print("Received message: " + message)

    if message.startswith("/66070276 "):
        command = message.split(" ")[1].strip()
        print("Command:", command)
        if command == "restconf":
            method = command
            responseMessage = "Ok: Restconf"
        elif command == "netconf":
            method = command
            responseMessage = "Ok: netconf"
        else:
            if method == "":
                if re.match(ip_pattern, command):
                    part = message.split(" ")
                    if len(part) == 3:
                        realcommand = part[2].strip()
                        if realcommand == "motd":
                            netmiko_final.device_ip=command
                            responseMessage = netmiko_final.motd()
                        else:
                            responseMessage = "Error: No method specified"
                    elif len(part) == 4:
                        motd = part[3].strip()
                        responseMessage = ansible_final.motd(command, motd)
                else:
                    responseMessage = "Error: No method specified"
            else:
                if re.match(ip_pattern, command):
                    
                    part = message.split(" ")
                    
                    if len(part) > 2:
                        realcommand = part[2].strip()
                        if method == "restconf":
                            restconf_final.router_ip = command
                            if realcommand == "create":
                                responseMessage = restconf_final.create()
                            elif realcommand == "delete":
                                responseMessage = restconf_final.delete()
                            elif realcommand == "enable":
                                responseMessage = restconf_final.enable()
                            elif realcommand == "disable":
                                responseMessage = restconf_final.disable()
                            elif realcommand == "status":
                                responseMessage = restconf_final.status()
                            elif realcommand == "motd":
                                if len(part) == 3:
                                    netmiko_final.device_ip=command
                                    responseMessage = netmiko_final.motd()
                                elif len(part) == 4:
                                    motd = part[3].strip()
                                    responseMessage = ansible_final.motd(command, motd)
                        elif method == "netconf":
                            netconf_final.ip = command
                            if realcommand == "create":
                                responseMessage = netconf_final.create()
                            elif realcommand == "delete":
                                responseMessage = netconf_final.delete()
                            elif realcommand == "enable":
                                responseMessage = netconf_final.enable()
                            elif realcommand == "disable":
                                responseMessage = netconf_final.disable()
                            elif realcommand == "status":
                                responseMessage = netconf_final.status()
                            elif realcommand == "motd":
                                if len(part) == 3:
                                    netmiko_final.device_ip=command
                                    responseMessage = netmiko_final.motd()
                                elif len(part) == 4:
                                    motd = part[3].strip()
                                    responseMessage = ansible_final.motd(command, motd)


                    else:
                        responseMessage = "Error: No command found."

                else:
                    responseMessage = "Error: No IP specified"
                    
        print(responseMessage)
        data = {"roomId": roomIdToGetMessages, "text": responseMessage}
        rp = requests.post(
            "https://webexapis.com/v1/messages",
            headers=getHTTPHeader,
            data=json.dumps(data)
            )
        if rp.status_code == 200:
            print("Message sent to Webex successfully")
        else:
            print(f"Error sending message: {rp.status_code}")