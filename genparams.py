#!/bin/env python3 
from base64 import b64encode
from os import environ
from json import dumps
from os.path import exists, join
from sys import argv, stderr, stdout
from string import Template

def slurp(filename, as_template=False):
    with open("cloud-config/" + filename, "r") as config:
        if as_template:
            # parse a YAML file and replace ${VALUE}s
            buffer = Template(config.read()).substitute(environ)
        else:
            buffer = config.read()
    # return b64encode(bytes(buffer, 'utf-8')).decode()
    return b64encode(bytes(buffer).encode('utf-8')).decode()

ADMIN_USERNAME = environ['ADMIN_USERNAME']
OWN_PUBKEY = join(environ['HOME'],'.ssh','id_rsa.pub')
GEN_PUBKEY = 'keys/' + ADMIN_USERNAME + '.pub'

if (environ.get('OWN_KEY','false').lower() == 'true') and exists(OWN_PUBKEY):
    admin_public_key = open(OWN_PUBKEY,'r').read()
    stderr.write('Warning: using %s instead of freshly generated keys.\n' % OWN_PUBKEY)
elif exists(GEN_PUBKEY):
    admin_public_key = open(GEN_PUBKEY,'r').read()
else:
    stderr.write('No public keys found, exiting.\n')
    exit(1)

params = {
    "adminUsername": {
        "value": ADMIN_USERNAME
    },
    "adminPublicKey": {
        "value": admin_public_key
    },
    "masterCount": { 
        "value": int(environ.get('MASTER_COUNT', 1))
    },
    "masterCustomData": {
        "value": slurp("master.yml")
    },
    "agentCount": {
        "value": int(environ.get('AGENT_COUNT', 2))
    },
    "agentCustomData": {
        "value": slurp("agent.yml")
    },
    "masterSize": {
        "value": "Standard_F2"
    },
    "agentSize": {
        "value": "Standard_F2"
    },
    "saType": {
        "value": "Standard_LRS"
    }
}

stdout.write(dumps(params))
