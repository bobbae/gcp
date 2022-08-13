# # netlify DNS nameservice
#
# Use netlify name servers to update via REST API. It does not have 
# restrictions for freenom domains like .cf, .ga, .gq, .ml or .tk.
#
# ```
# # get zones
#
# curl  -H "Authorization: Bearer ${NETLIFY_TOKEN}" https://api.netlify.com/api/v1/dns_zones|jq .
#
# # using one of the zones, update A record
#
# curl -XPOST -H "Authorization: Bearer ${NETLIFY_TOKEN}" \
#        -H "Content-Type: application/json" \
#        https://api.netlify.com/api/v1/dns_zones/${NETLIFY_ZONE_ID}/dns_records \
#        -d '{ "type":"A", "hostname":"mynode", "value":"34.34.23.123" }'
# ```

import subprocess
import json
import argparse
import os
import requests

args = None

def main():
    global args
    parser = argparse.ArgumentParser(
        description='update netlify dns records')

    parser.add_argument('Domain',
                        metavar='domain',
                        type=str,
                        help='domain to update')
    
    parser.add_argument('--dryrun',
                        action='store_true',
                        help='dry run')
    
    parser.add_argument('--kind',
                        action='store',
                        type=str,
                        default='A',
                        help='type of record, e.g. A')
    
    parser.add_argument('--zone',
                        action='store',
                        type=str,
                        help='dns zone')
    
    parser.add_argument('--api-token',
                        action='store',
                        type=str,
                        help='API token')
    
    parser.add_argument('--a-name',
                        action='store',
                        type=str,
                        help='record  A name')
    
    parser.add_argument('--a-ip',
                        action='store',
                        type=str,
                        help='record  A IP')
    
    args = parser.parse_args()

    domain = args.Domain

    if (args.api_token == None):
        atoken = os.getenv('NETLIFY_TOKEN')
        if (atoken == None):
            print("can't find NETLIFY_TOKEN")
            os.exit(1)
        args.api_token = atoken

    if (args.zone== None):
        azone = os.getenv('NETLIFY_ZONE_ID')
        if (azone== None):
            print("can't find NETLIFY_ZONE_ID")
            os.exit(1)
        args.zone = azone

    find_gcp_vms_ip(callback1)

def find_gcp_vms_ip(cb):
    instances = subprocess.Popen(['gcloud', 'compute', 'instances', 'list', '--format=json'], stdout=subprocess.PIPE).communicate()[0]
    instances2 = json.loads(instances.decode('utf-8').replace('\n', ' '))
    for inst in instances2:
        name = inst['name']
        interface = inst['networkInterfaces'][0]
        if (interface == None):
            return
        accessConfigs = interface['accessConfigs']
        if (accessConfigs == None):
            return
        externalIP = accessConfigs[0]['natIP']
        if (externalIP == None):
            return
        cb(name,externalIP)

def netlify_get_zones():
    url = "https://api.netlify.com/api/v1/dns_zones"
    bearer_token = f"Bearer {args.api_token}"

    headers = {
        'Authorization': bearer_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(
        url,
        headers=headers
    )
    print(response.text)
    
    
def netlify_update(name,ip,domain):
    url = f"https://api.netlify.com/api/v1/dns_zones/{args.zone}/dns_records"
    bearer_token = f"Bearer {args.api_token}"

    headers = {
        'Authorization': bearer_token,
        'Content-Type': 'application/json'
    }
    data = {
        'type': args.kind,
        'hostname': name,
        'value': ip
    }
    response = requests.post(
        url,
        headers=headers,
        data=data
    )
    print(response.text)

def callback1(name,externalIP):
    #print(args)
    #print(name,externalIP)
    netlify_get_zones()
    netlify_update(name,externalIP,args.Domain)

if __name__ == "__main__":
    main()
