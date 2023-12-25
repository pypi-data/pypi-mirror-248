#!/usr/bin/env python
"""
Flexi Mange Client API 
Usage: 
    flexiclient --manage=manage_name login [--username=user] [--password==password]
    flexiclient --manage=manage_name logout
    flexiclient --manage=manage_name create_organization [--org_name=scale] [--encryption_method=ikev2]
    flexiclient --manage=manage_name delete_organization [--org_name=scale] 
    flexiclient --manage=manage_name get_device_list [--org_name=pnc]
    flexiclient --manage=manage_name get_org_list
    flexiclient --manage=manage_name approve_devices [--org_name=pnc]
    flexiclient --manage=manage_name delete_devices [--org_name=scale] 
    flexiclient --manage=manage_name get_access_key [--key_name=key_name]    
    flexiclient --manage=manage_name create_org_token [--org_name=scale] [--key_name=key_name]
    flexiclient --manage=manage_name create_access_key [--key_name=key_name]    
    flexiclient --manage=manage_name delete_access_key [--key_name=key_name]
    flexiclient --manage=manage_name create_simulator [--count=100] [--repo=setup] [--version=latest] [--conf_file=fw-image.pkr.json]
    flexiclient --manage=manage_name create_snapshot [--provider=hetzner] [--repo=setup] [--version='4.1.12'] [--api_id=pugazht] [--api_token=dasdfasfsd] [--conf_file=simulator.hcloud.pkr.json] 
    flexiclient --manage=manage_name create_instances [--provider=hetzner] [--count=<number>] [--lan_network='10.0.0.0/16'] [--prefix=8] [--api_id=pugazht]
    flexiclient --manage=manage_name destroy_instances [--provider=hetzner] [--api_id=<devops>]
    flexiclient --manage=manage_name create_instances_dry_run [--provider=hetzner] [--count=<number>] [--lan_network='10.0.0.0/24'] [--prefix=6]
    flexiclient --manage=manage_name add_pathlabels [--labels_count=32] [--org_name=scale]
    flexiclient --manage=manage_name assign_pathlabels [--org_name=scale] [--path_label=label_name]
    flexiclient --manage=manage_name delete_pathlabels [--org_name=scale]
    flexiclient --manage=manage_name get_tunnels [--org_name=scale]
    flexiclient --manage=manage_name delete_tunnels [--org_name=scale] [--count=10]

Arguments:
  Options:
  -h --help
"""

import requests
import sys
import os
import errno
import getpass
import urllib.parse as urlparse
import urllib
import subprocess
import json
import docopt, random


VERIFY_CERT=False
AUTOMATION_ROOT='/root/flexitests/'
HZ_CLOUD=AUTOMATION_ROOT + 'infra/hetzner_cloud/'
DO_CLOUD=AUTOMATION_ROOT + 'infra/digital_ocean/'
HZ_PACKER_SIMULATOR_DIR=HZ_CLOUD + 'simulator-scale/images/'
HZ_TF_SIMULATOR_DIR=HZ_CLOUD + 'simulator-scale/instances/'
HZ_PACKER_DIR=HZ_CLOUD + 'images/'
DO_PACKER_DIR=DO_CLOUD + 'images/'
HZ_TF_DIR=HZ_CLOUD + 'instance/'
HZ_SN_DIR=HZ_CLOUD + 'snaphot/'
#HZ_TF_DIR=HZ_CLOUD + 'pugazht/' + 'instances/'
DO_TF_DIR=DO_CLOUD + 'instances/'

#------------------------------------------------------------------------
def _config_fname(manage):
    return os.path.expanduser( "~/.manage_%s" % manage)

#------------------------------------------------------------------------
def _manage_url(manage, path):
    return urlparse.urlunsplit( ("https", manage, path, "", "" ))

#------------------------------------------------------------------------
def _manage_get_token(manage):
    with open(_config_fname(manage)) as conf:
       return conf.read()

#------------------------------------------------------------------------
def _call_fleximanage(manage, method, uri, payload):
    url = _manage_url(manage, uri)
    token = _manage_get_token(manage)
    
    headers = {
      'Authorization' : f'Bearer {token}',
      'Content-Type' : 'application/json'
    }
    if method == "GET":
        response = requests.request(method, url, headers=headers)
    elif method == "POST":
        response = requests.request(method, url, headers=headers, data=payload)
    elif method == "PUT":
        response = requests.request(method, url, headers=headers, data=payload)
    elif method == "DELETE":
        response = requests.request(method, url, headers=headers)

    return response

#------------------------------------------------------------------------
def do_login(manage, args):
    user = args["--username"]
    passwd = args["--password"]
    if not user: user = input("Login: ")
    if not passwd: passwd = getpass.getpass("Password: ")
    payload = urlparse.urlencode({ 'username': user, 'password': passwd})
    headers = {
      'Authorization': 'Bearer null',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post( 
         _manage_url( manage, "/api/users/login"),
         headers=headers,
         data=payload,
         allow_redirects=False,
         verify=VERIFY_CERT
       )
    print(r.text)
    #print(r.headers["refresh-jwt"])
    if "refresh-jwt" not in r.headers:
        raise RuntimeError("token is not valid")

    with os.fdopen(os.open(_config_fname(manage), os.O_WRONLY | os.O_CREAT, 600), 'w') as conf :
         conf.write(r.headers["refresh-jwt"])

#------------------------------------------------------------------------

def get_device_list(manage, args):
    org_id = get_org_id(manage, args)
    r = _call_fleximanage(manage, "GET", f"api/devices?org={org_id}", payload='none')
    devices = json.loads(r.text)
    print(r.status_code)
    #print(devices)
    if r.status_code != 500:
        #for device in devices:
            #print(device['name'] + "--" + device['machineId'])
            #print(json.dumps(device, indent=4))
        return devices

def get_org_id(manage, args):
    org_name = args["--org_name"]
    r = _call_fleximanage(manage, "GET", "api/organizations", payload='none')
    print(r.status_code)
    if r.status_code == 200:
        orgs = json.loads(r.text)
        print(orgs)
        for org in orgs:
            if org_name == org["name"]:
                org_id = org["_id"]
                return org_id
        else:
            print(f"Error: Organization not found \n Available Organizations are : {r.content}")
    else:
        print(f"Error: while fetching organization information: {r.text}")

#-------------------------------------------------------------------------
def create_organization(manage, args):
    org_name = args["--org_name"]
    encryption_method = args["--encryption_method"]
    payload = json.dumps({"name": org_name, "description": org_name, "group": "Default", "encryptionMethod": encryption_method})
    print(payload)
    r = _call_fleximanage(manage, "POST", f"api/organizations", payload=payload)
    if r.status_code == 201:
        org = json.loads(r.content)
        print(f"The Organization with Name: {org_name} Created and it's info : {org}")
    else:
        print(f"Error while creating Organization: {r.text}")

#---------------------------------------------------------------------------

def delete_organization(manage, args):
    org_id = get_org_id(manage, args)
    r = _call_fleximanage(manage, "DELETE", f"api/organizations/{org_id}", payload='none')
    if r.status_code == 204:
        print(f"The Organization with ID: {org_id} Deleted successfully")
    else:
        print(f"Error while deleting specified Orgnization: {r.text}")

def get_tunnels(manage, args):
    org_name = args["--org_name"]
    r = _call_fleximanage(manage, "GET", "api/tunnels", payload='none')
    if r.status_code == 200:
        tunnels = json.loads(r.text)
        #print(tunnels)
    return tunnels

#-------------------------------------------------------------------------

def delete_tunnels(manage, args):
    tunnels = get_tunnels(manage, args)
    org_id = get_org_id(manage, args)
    count = args["--count"]
    i = 0
    del_tunnels = {}
    for tunnel in tunnels:
        #payload = f"\{\"method\":\"deltunnels\", \"tunnels\":\{{tunnel['_id']}:true\}, \"filters\":null \}" 
        del_tunnels.update({tunnel['_id']:True})
        i=i+1
        if (i == int(count)):
            break
    else:
        print("There is no satisfying number of tunnels!")
    payload = json.dumps({"method":"deltunnels", "tunnels":del_tunnels, "filters":"null"})
    print(payload)
    r = _call_fleximanage(manage, "POST", f"api/devices/apply?org={org_id}", payload=payload)
    if r.status_code == 202:
        print(f"{count} Tunnels were deleted which Id is {del_tunnels}")
    else:
        print(f"Error encountered while deleting Tunnels: {r.text}")
        

#----------------------------------------------------------------------------        

def approve_devices(manage, args):
    devices = get_device_list(manage, args)
    count = 1
    for device in devices:
        if device['hostname'] is not None and device['name'] == "":
            device['name'] = device['hostname'] + str(count)
            device['description'] = device['hostname'] + str(count)
            print(f"Device {device['name']} is Updated!")
        if not device['isApproved']:
            device['isApproved'] = True
        org = device['org']
        r = _call_fleximanage(manage, "PUT", f"api/devices/{device['_id']}?org={org}", payload=json.dumps(device))
        if r.status_code == 204 or r.status_code == 200:
            print(f"Device {device['name']} is Approved!")
        else:
            print(f"device {device['name']} is not approved")
            print(r.text)
        count = count + 1       
    assign_interfaces(manage, args) 

def assign_interfaces(manage, args):
    devices = get_device_list(manage, args)
    for device in devices:
        #print(device['description'])
        if device['isApproved']:
            interfaces = device['interfaces']
            for interface in interfaces:
                if not interface['isAssigned']:
                    interface['isAssigned'] = True
        print(device)
        org = device['org']
        r = _call_fleximanage(manage, "PUT", f"api/devices/{device['_id']}?org={org}", payload=json.dumps(device))
        print(r.status_code)
        print(r.text)

def delete_edge_devices(manage, args):
    devices = get_device_list(manage, args)
    for device in devices:
        print(device)
        org = device['org']
        r = _call_fleximanage(manage, "DELETE", f"api/devices/{device['_id']}?org={org}", payload=json.dumps(device))
        print(r.status_code)
        if r.status_code == 200 or r.status_code == 204:
            print(f"Device {device['name']} is Deleted from flexi Manage Successfully!")

def get_org_list(manage, args):
    orgs = _call_fleximanage(manage, "GET", "api/organizations", payload='none')
    #print(json.dumps(r, indent=4))
    for org in json.loads(orgs.text):
        print(org)
#------------------------------------------------------------------------
def get_access_key(manage, args):
    keys = json.loads(_call_fleximanage(manage, "GET", "api/accesstokens", payload='none').text)
    access_key = "" 
    for key in keys:
        if key["name"] == args["--key_name"]:
            access_key = key["token"]
            print(access_key)
            os.remove(_config_fname(manage))
            with os.fdopen(os.open(_config_fname(manage), os.O_WRONLY | os.O_CREAT, 600), 'w') as conf :
                conf.write(access_key)
            return access_key
        else:
            access_key = None
    if access_key == None:    
        print(f"Specified key name does not exists")

#------------------------------------------------------------------------
def get_access_key_id(manage, args):
    keys = json.loads(_call_fleximanage(manage, "GET", "api/accesstokens", payload='none').text)
    access_key_id = "" 
    for key in keys:
        if key["name"] == args["--key_name"]:
            access_key_id = key["_id"]
            print(access_key_id)
            return access_key_id
        else:
            access_key_id = None
    if access_key_id == None:    
        print(f"Specified key name does not exists")

#-----------------------------------------------------------------------------
def add_pathlabels(manage, args):
    #edge_count = int(args["--edge_count"])
    labels_count = int(args["--labels_count"])
    org_id = get_org_id(manage, args)
    digits = len(str(labels_count))
    current_labels = len(get_pathlabels(manage, args))
    for l in range(current_labels, labels_count):
        rand = lambda: random.randint(0,255)
        color = '#{:02x}{:02x}{:02x}'.format(rand(), rand(), rand())
        label = "path-label-" + str(l+1).zfill(digits)
        payload = json.dumps({"name":label,"description":label,"color":color,"type":"Tunnel"})
        r = _call_fleximanage(manage, "POST", f"api/pathlabels?org={org_id}", payload=payload)
        print(r.text)
        if r.status_code == 201:
            print(f"Path Lable {label} created successfully")

def get_pathlabel_data(manage, path_label_name="all"):
    resp = _call_fleximanage(manage, "GET", f"api/pathlabels", payload="none")
    path_labels = []
    path_label_data = {}
    if resp.status_code == 200: 
        print("Got all the path labels")
        path_labels = json.loads(resp.text)
    if path_label_name == "all":
        path_label_data = path_labels
        return path_label_data
    else:
        print(f"Getting specific path label data for {path_label_name}")
        for path_label in path_labels: 
            if path_label_name == path_label["name"]:
                path_label_data = path_label
        return path_label_data

def get_device_id(manage, device_name, org_name):
    args = {}
    args["--org_name"] = org_name
    args["--device_name"] = device_name
    devices = get_device_list(manage, args)
    device_id = 0
    for device in devices:
        if device_name == device["name"]:
            device_id = device["_id"]
            break
    return device_id

def get_device_configuration(manage, device_name, org_name):
    device_id = get_device_id(manage, device_name=device_name, org_name=org_name)
    device_config = {}
    resp = _call_fleximanage(manage, "GET", f"api/devices/{device_id}", payload="none")
    print(json.loads(resp.text))
    print(resp.status_code)
    if resp.status_code == 200:
        device_config = json.loads(resp.text)[0]
        return device_config
    else:
        print(f"Device name {device_name} is not found")

def assign_pathlabels(manage, args):
    org_name = args["--org_name"]
    path_label = args["--path_label"]
    org_id = get_org_id(manage, args)
    #device_name = args["--device_name"]
    devices_list = get_device_list(manage, args)
    for device in devices_list:
        device_name = device['name']
        device_id = device['_id']
        config = get_device_configuration(manage, device_name, org_name)
        #device_id = get_device_id(manage, device_name, org_name)
        #print(config[0].get('interfaces'))
        interfaces = config.get("interfaces")
        path_label_data = get_pathlabel_data(manage, path_label_name=path_label)
        print(f"Path label data: {path_label_data}")
        for interface in interfaces:
            if interface["type"] == "WAN":
                interface["pathlabels"].append(path_label_data)
        #print(interfaces)
        config.update({"interfaces": interfaces})
        #print(json.dumps(config))
        payload = json.dumps(config)
        print(f"Payload is : {payload}")
        resp = _call_fleximanage(manage, "PUT", f"api/devices/{device_id}?org={org_id}", payload=payload)
        #print(resp.status_code)
        #print(resp.text)
        if resp.status_code == 202:
            print(f"Path labels assigned to the device {device_name} WAN interface")
            print(f"Device Updated with path labels: {resp.text}")

def get_pathlabels(manage, args):
    #label_name = args["--label_name"]
    r = _call_fleximanage(manage, "GET", "api/pathlabels", payload='none')
    labels = json.loads(r.text)
    return labels    

def delete_pathlabels(manage, args):
    #if not args.has_key("--label_name"): 
    org_name = args["--org_name"]
    labels = get_pathlabels(manage, args)
    org_id = get_org_id(manage, args)
    print(labels)
    for label in labels:
        print(label["name"])
        resp = _call_fleximanage(manage, "DELETE", f"api/pathlabels/{label['_id']}?org={org_id}", payload='none')
        print(resp.text)
        if resp.status_code == 204:
            print(f"Path label {label['name']} deleted successfully")

def create_tunnels(manage, args):
    #labels = get_pathlabels(manage,args)
    spoke = get_device_id(manage, args["--spoke"], args["--org_name"])
    hub = get_device_id(manage, args["--hub"], args["--org_name"])
    payload = json.dumps({"method":"tunnels","devices":{f"{spoke}":True, f"{hub}":True},"tunnelType":"site-to-site","meta":{"pathLabels":["FFFFFF"]}})
    resp = _call_fleximanage(manage, "POST", "api/devices/apply", payload=payload)
    if resp.status_code == 202:
        key = json.loads(resp.text)
        print(key)

def create_access_key(manage, args):
    payload = json.dumps({ 'name': args["--key_name"], 'validityEntity': 'Default'})
    resp = _call_fleximanage(manage, "POST", "api/accesstokens", payload=payload)
    #key = {}
    if resp.status_code == 201:
        key = json.loads(resp.text)
        print(f"Access key with Name: {key['name']} is created Successfully")
        print(f"It's Token is : {key['token']}")
        if os.path.isfile(_config_fname(manage)):
            os.remove(_config_fname(manage))
            with os.fdopen(os.open(_config_fname(manage), os.O_WRONLY | os.O_CREAT, 600), 'w') as conf :
                conf.write(key['token'])    
        return key['token']
    else:
        #key = None
        print("Access key is not created")    

def create_org_token(manage, args):
    org_id = get_org_id(manage, args)
    key_name = args["--key_name"]
    payload = json.dumps({ 'name': args["--key_name"], 'server': ''})
    resp = _call_fleximanage(manage, "POST", f"api/tokens?org={org_id}", payload=payload)
    if resp.status_code == 201:
        key = json.loads(resp.text)
        print(f"Organization token with Name: {key['name']} is created Successfully")
        print(f"It's Token is : {key['token']}")
        user_data = HZ_CLOUD + 'modules/' + 'instance/' + 'flexiwan-user-data'
        user_data_template = HZ_CLOUD + 'dataplane_scale/' + 'flexiwan-user-data-scale-template'
        if os.path.isfile(user_data):
            file = open(user_data, "r")
            new_file = ""
            for line in file:
                new_line = line.replace("{{ token }}", key['token'])
                new_file += new_line 
            file.close()
            with os.fdopen(os.open(user_data_template, os.O_WRONLY | os.O_CREAT, 600), 'w') as conf :
                conf.write(new_file)
                conf.close()
            print("Organization user-data file is succesfully created")
    else:
        #key = None
        print("Organization token is not created")    


def delete_access_key(manage, args):
    key_id = get_access_key_id(manage, args)
    url = "api/accesstokens/" + key_id
    resp = _call_fleximanage(manage, "DELETE", url, payload='none')
    if resp.status_code == 204:
        print("Key is successfully Deleted")

def create_snapshot(manage, args):
    provider = args['--provider']
    version = args['--version']
    repo = args['--repo']
    cfile = args['--conf_file']
    api_id = args['--api_id']
    api_token = args['--api_token']
    #packer build -var "version=4.1.12" -var "repo=setup" -var "api_token=" images/fw-image.pkr.json
    if provider == 'hetzner':
        print("Creating Snapshot of Flexiwan router in Hetzner Cloud")
        HZ_PACKER_DIR = HZ_CLOUD + 'modules/' + 'images/'
        packer_run = subprocess.Popen(['packer', 'build', '-var', f"version={version}", '-var', f"repo={repo}", '-var', f"api_id={api_id}", '-var', f"api_token={api_token}", f"{HZ_PACKER_DIR}{cfile}"])
        packer_run.wait()
        jfile = open(HZ_CLOUD + 'modules/' + 'snapshot/' + f'fw-router-{api_id}-manifest.json')
        js_object = json.load(jfile)
        artifacts = js_object['builds']
        last_run_uuid = js_object['last_run_uuid']
        jfile.close()
        for artifact in artifacts:
            if artifact['packer_run_uuid'] == last_run_uuid:
                artifact_id = artifact['artifact_id']
                token = artifact['custom_data']['token']
    elif provider == 'digital-ocean':
        print("Creating Snapshot of Flexiwan router in Digital Ocean Cloud")
        packer_run = subprocess.Popen(['packer', 'build', '-var', f"version={version}", '-var', f"repo={repo}", f"{DO_PACKER_DIR}{cfile}"])
        packer_run.wait()
        jfile = open(DO_PACKER_DIR + f'fw-router-{version}-manifest.json')
        js_object = json.load(jfile)
        artifacts = js_object['builds']
        last_run_uuid = js_object['last_run_uuid']
        jfile.close()
        for artifact in artifacts:
            if artifact['packer_run_uuid'] == last_run_uuid:
                artifact_id = artifact['artifact_id']
                print(artifact_id)

def create_instances(manage, args):
    provider = args['--provider']
    count = args['--count']
    lan_network = args['--lan_network']
    prefix = args['--prefix']
    api_id = args['--api_id']
    if provider == 'hetzner':
        HZ_TF_DIR = HZ_CLOUD + 'dataplane_scale/'
        jfile = open(HZ_CLOUD + 'modules/' + 'snapshot/' + f'fw-router-{api_id}-manifest.json')
        js_object = json.load(jfile)
        artifacts = js_object['builds']
        artifcat_id = token = ""
        last_run_uuid = js_object['last_run_uuid']
        jfile.close()
        for artifact in artifacts:
            if artifact['packer_run_uuid'] == last_run_uuid:
                artifact_id = artifact['artifact_id']
                token = artifact['custom_data']['token']
        if artifact_id and token: 
            print("Terraform Got the Snapshot ID and Token from the Packer file")
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to create instance in Hetzner Cloud")
        os.chdir(HZ_TF_DIR)
        tf_init = subprocess.Popen(['terraform', 'init'])
        tf_init.wait()
        print(tf_init.returncode)
        print("Running Terraform Plan")
        tf_plan = subprocess.Popen(['terraform', 'plan', '-var', f"hcloud_token={token}", '-var', f"snapshot_id={artifact_id}", '-var', f"instance_count={count}", '-var', f"lan_network={lan_network}", '-var', f"lan_network_prefix={prefix}",  f"-out=hcloud_{api_id}_plan"])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan")
        tf_apply = subprocess.Popen(['terraform', 'apply', f"hcloud_{api_id}_plan"])
        tf_apply.wait()
        print(tf_apply.returncode)
    elif provider == 'digital_ocean':
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to create instance in Digital Ocean")
        os.chdir(DO_TF_DIR)
        tf_init = subprocess.Popen(['terraform', 'init'])
        tf_init.wait()
        print(tf_init.returncode)
        print(f"Running Terraform Plan to create {count} instance(s)")
        tf_plan = subprocess.Popen(['terraform', 'plan', '-var', f"instance_count={count}", '-var', f"lan_network={lan_network}", '-var', f"lan_network_prefix={prefix}", "-out=hcloud_plan"])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan to create {count} instance(s)")
        tf_apply = subprocess.Popen(['terraform', 'apply', "hcloud_plan"])
        tf_apply.wait()
        print(tf_apply.returncode)

def destroy_instances(manage, args):
    provider = args['--provider']
    api_id = args['--api_id']
    HZ_TF_DIR = HZ_CLOUD + 'dataplane_scale/'
    if provider == 'hetzner':
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to delete instance in Hetzner Cloud")
        os.chdir(HZ_TF_DIR)
        tf_plan = subprocess.Popen(['terraform', 'plan', '-destroy', f'-out=hcloud_{api_id}_plan'])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan to delete the created instance")
        tf_apply = subprocess.Popen(['terraform', 'apply', f'hcloud_{api_id}_plan'])
        tf_apply.wait()
        print(tf_apply.returncode)
    elif provider == 'digital_ocean':
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to delete instance in Digital Ocean")
        os.chdir(DO_TF_DIR)
        print(f"Running Terraform Plan to delete instance(s)")
        tf_plan = subprocess.Popen(['terraform', 'plan', '-delete', "-out=hcloud_plan"])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan to delete instance(s)")
        tf_apply = subprocess.Popen(['terraform', 'apply', "hcloud_plan"])
        tf_apply.wait()
        print(tf_apply.returncode)

def destroy_instances(manage, args):
    provider = args['--provider']
    api_id = args['--api_id']
    HZ_TF_DIR = HZ_CLOUD + 'dataplane_scale/'
    if provider == 'hetzner':
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to delete instance in Hetzner Cloud")
        os.chdir(HZ_TF_DIR)
        tf_plan = subprocess.Popen(['terraform', 'plan', '-destroy', f'-out=hcloud_{api_id}_plan'])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan to delete the created instance")
        tf_apply = subprocess.Popen(['terraform', 'apply', f'hcloud_{api_id}_plan'])
        tf_apply.wait()
        print(tf_apply.returncode)
    elif provider == 'digital_ocean':
        #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
        print("Terraform Initialization to delete instance in Digital Ocean")
        os.chdir(DO_TF_DIR)
        print(f"Running Terraform Plan to delete instance(s)")
        tf_plan = subprocess.Popen(['terraform', 'plan', '-delete', "-out=hcloud_plan"])
        tf_plan.wait()
        print(tf_plan.returncode)
        print("Apply the Terraform Plan to delete instance(s)")
        tf_apply = subprocess.Popen(['terraform', 'apply', "hcloud_plan"])
        tf_apply.wait()
        print(tf_apply.returncode)

def  create_instances_dry_run(manage, args):
    count = args['--count']
    path = args['--path']
    lan_network = args['--lan_network']
    prefix = args['--prefix']
    HZ_TF_DIR = HZ_CLOUD + 'instances/' + path
    #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
    print("Terraform Initialization")
    os.chdir(HZ_TF_DIR)
    tf_init = subprocess.Popen(['terraform', 'init'])
    tf_init.wait()
    print(tf_init.returncode)
    print("Running Terraform Plan")
    tf_plan = subprocess.Popen(['terraform', 'plan', '-var', f"instance_count={count}", '-var', f"lan_network={lan_network}", '-var', f"lan_network_prefix={prefix}", "-out=hcloud_plan"])
    tf_plan.wait()
    print(tf_plan.returncode)

def  create_simulator(manage, args):
    count = args['--count']
    path = args['--path']
    lan_network = args['--lan_network']
    prefix = args['--prefix']
    HZ_TF_DIR = HZ_CLOUD + 'instances/' + path
    #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
    #provider = args['--provider']
    version = args['--version']
    repo = args['--repo']
    cfile = args['--conf_file']
    #packer build -var "version=4.1.12" -var "repo=setup" images/fw-image.pkr.json
    #if provider == 'hetzner':
    print("Creating Snapshot of Flexiwan router in Hetzner Cloud for Simulator")
    packer_run = subprocess.Popen(['packer', 'build', '-var', f"version={version}", '-var', f"repo={repo}", f"{HZ_PACKER_SIMULATOR_DIR}{cfile}"])
    packer_run.wait()
    jfile = open(HZ_PACKER_SIMULATOR_DIR + f'fw-router-{version}-manifest.json')
    js_object = json.load(jfile)
    artifacts = js_object['builds']
    last_run_uuid = js_object['last_run_uuid']
    jfile.close()
    for artifact in artifacts:
        if artifact['packer_run_uuid'] == last_run_uuid:
            artifact_id = artifact['artifact_id']
            print(artifact_id)
            os.environ['TF_VAR_HCLOUD_LAST_SNAPSHOT_ID'] = artifact_id
    print(f"The Environment Variable HCLOUD_LAST_SNAPSHOT_ID : {os.getenv('TF_VAR_HCLOUD_LAST_SNAPSHOT_ID')}")
    print("Terraform Initialization")
    os.chdir(HZ_TF_DIR)
    tf_init = subprocess.Popen(['terraform', 'init'])
    tf_init.wait()
    print(tf_init.returncode)
    print("Running Terraform Plan")
    tf_plan = subprocess.Popen(['terraform', 'plan', '-var', f"instance_count={count}", "-out=hcloud_simulator_plan"])
    tf_plan.wait()
    print(tf_plan.returncode)

def  create_simulator(manage, args):
    count = args['--count']
    #lan_network = args['--lan_network']
    #prefix = args['--prefix']
    #cd /root/pugazht/flexitests/infra/hetzner-cloud/instances/ ; terraform plan -var 'instance_count=10' -var 'lan_network=10.0.0.0/24' -var 'lan_network_prefix=6' -out=hcloud_plan
    #provider = args['--provider']
    version = args['--version']
    repo = args['--repo']
    cfile = args['--conf_file']
    #packer build -var "version=4.1.12" -var "repo=setup" images/fw-image.pkr.json
    #if provider == 'hetzner':
    print("Creating Snapshot of Flexiwan router in Hetzner Cloud for Simulator")
    packer_run = subprocess.Popen(['packer', 'build', '-var', f"version={version}", '-var', f"repo={repo}", f"{HZ_PACKER_SIMULATOR_DIR}{cfile}"])
    packer_run.wait()
    jfile = open(HZ_PACKER_SIMULATOR_DIR + f'fw-router-{version}-manifest.json')
    js_object = json.load(jfile)
    artifacts = js_object['builds']
    last_run_uuid = js_object['last_run_uuid']
    jfile.close()
    for artifact in artifacts:
        if artifact['packer_run_uuid'] == last_run_uuid:
            artifact_id = artifact['artifact_id']
            print(artifact_id)
            os.environ['TF_VAR_HCLOUD_LAST_SNAPSHOT_ID'] = artifact_id
    print(f"The Environment Variable HCLOUD_LAST_SNAPSHOT_ID : {os.getenv('TF_VAR_HCLOUD_LAST_SNAPSHOT_ID')}")
    print("Terraform Initialization")
    os.chdir(HZ_TF_SIMULATOR_DIR)
    tf_init = subprocess.Popen(['terraform', 'init'])
    tf_init.wait()
    print(tf_init.returncode)
    print("Running Terraform Plan")
    tf_plan = subprocess.Popen(['terraform', 'plan', '-var', f"instance_count={count}", "-out=hcloud_simulator_plan"])
    tf_plan.wait()
    print(tf_plan.returncode)
    
_function_map = {
    "login":do_login,
    "create_organization":create_organization,
    "delete_organization":delete_organization,
    "get_device_list":get_device_list,
    "get_org_list":get_org_list,
    "get_access_key":get_access_key,
    "create_access_key":create_access_key,
    "delete_access_key":delete_access_key,
    "create_org_token":create_org_token,
    "create_snapshot":create_snapshot,
    "create_simulator":create_simulator,
    "create_instances":create_instances,
    "add_pathlabels":add_pathlabels,
    "assign_pathlabels":assign_pathlabels,
    "delete_pathlabels":delete_pathlabels,
    "destroy_instances":destroy_instances,
    "create_instances_dry_run":create_instances_dry_run,
    "approve_devices":approve_devices,
    "delete_devices":delete_edge_devices,
    "get_tunnels":get_tunnels,
    "delete_tunnels":delete_tunnels
}

#------------------------------------------------------------------------
if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    manage = args["--manage"]
    try:
        _function_map[sys.argv[2]](manage, args)
    except RuntimeError as e:
        print(sys.stderr, e.message)
        sys.exit(1)
