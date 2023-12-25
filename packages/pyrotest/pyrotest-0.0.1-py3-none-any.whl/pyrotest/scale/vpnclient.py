#!/usr/bin/env python
"""
Remote VPN Client API 
Usage: 
    vpnclient --manage=manage_name login [--username=user] [--password=password] [--workspace=workspace_name]
    vpnclient --manage=manage_name logout
    vpnclient --manage=manage_name get_vpn_profile 
  

Arguments:
  Options:
  -h --help
"""

import requests
import sys
import os
import getpass
import urllib.parse as urlparse
import json
import docopt


VERIFY_CERT=False
AUTOMATION_ROOT='/root/flexitests/'
user="pugazht@flexiwan.com"
passwd="Y@@thiish"
workspace="simvpn"


#------------------------------------------------------------------------
def _config_fname(manage):
    return os.path.expanduser( "~/.vpnqa_%s" % manage)

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
    #print(headers)
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
    workspace = args["--workspace"]
    if not user: user = input("Login: ")
    if not passwd: passwd = getpass.getpass("Password: ")
    if not workspace: workspace = input("Workspace: ")
    payload = urlparse.urlencode({ 'username': user, 'password': passwd, 'workspace': workspace})
    headers = {
      'Authorization': 'Bearer null',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post( 
         _manage_url( manage, "/api/login/flexiManage"),
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

def get_vpn_profile(manage, args):
    keys = json.loads(_call_fleximanage(manage, "GET", "api/resources/config?responseType=json", payload='none').text)
    access_key = "" 
    token = _manage_get_token(manage)
    print(token)
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, workspace)):
        os.makedirs(os.path.join(cwd, workspace))
        print(f'{workspace} directory is created')
    for key in keys:
        print(key)
        if key == 'config':
           fname=workspace + '.ovpn'
           with open(os.path.join(cwd, workspace, fname), 'w') as fp:
               fp.write(keys.get(key))
               fp.close()
        elif key == 'email':
            fname='token'
            with open(os.path.join(cwd, workspace, fname), 'w') as fp:
                fp.write(keys.get(key) + ' \n')
                fp.write(token)
                fp.close()
            print(token)
        else:
            with open(os.path.join(cwd, workspace, key), 'w') as fp:
               fp.write(keys.get(key))
               fp.close()

_function_map = {
    "login":do_login, 
    "get_vpn_profile":get_vpn_profile
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
