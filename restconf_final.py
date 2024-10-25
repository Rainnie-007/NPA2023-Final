import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.189
api_url = "https://10.0.15.189/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070193"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {"Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
  "ietf-interfaces:interface": {
    "name": "Loopback65070193",
    "description": "My first RESTCONF loopback",
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "172.30.193.1",
          "netmask": "255.255.255.0"
        }
      ]
    }
  }
}

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Loopback Interface Created"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete():
    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Loopback Interface Deleted"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def enable():
    yangConfig = {"ietf-interfaces:interface": {
    "name": "Loopback65070193",
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    }}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Loopback Interface Enabled"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def disable():
    yangConfig = {"ietf-interfaces:interface": {
    "name": "Loopback65070193",
    "type": "iana-if-type:softwareLoopback",
    "enabled": False,
    }}


    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Loopback Interface Disabled"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def status():
    api_url_status = "https://10.0.15.189/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070193"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json['ietf-interfaces:interface']['admin-status']
        oper_status = response_json['ietf-interfaces:interface']['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return "Interface is up and running"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface is down"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "Interface not found"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
