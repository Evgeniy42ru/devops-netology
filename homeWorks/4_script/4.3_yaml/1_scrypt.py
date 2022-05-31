#!/usr/bin/env python3


import json
import socket
import yaml


needChangeIps = False

with open('hosts.json') as json_file:
    hosts = json.load(json_file)

for host in hosts:
    ipActual = socket.gethostbyname(host)
    
    if hosts[host] != ipActual:
        print("[ERROR] {} IP mismatch: {} {}".format(host, hosts[host], ipActual))
        hosts[host] = ipActual
        needChangeIps = True
    else:
        print("{} - {}".format(host, hosts[host]))

if needChangeIps == True:
    with open('hosts.json', 'w') as outfile:
        json.dump(hosts, outfile)

    with open('hosts.yaml', 'w') as outfile:
        yaml.dump(hosts, outfile)