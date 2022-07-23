# Read data from a URL and store the data into a GCS blob
#
# Download and point to the service account credential file.
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/bob/service-account-1-84f3.json 
#
# Then run python req.py -p projectid -b bucketid -f filename
#

import argparse
import sys
import requests
from google.cloud  import storage as gcs

parser = argparse.ArgumentParser(description="read from URL and store to GCS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--project", default="", help="project")
parser.add_argument("-b", "--bucket", default="", help="bucket")
parser.add_argument("-f", "--filename", default="", help="filename")


#print(r.text)

args = parser.parse_args()
config = vars(args)
print("config",config)

config_project = config["project"]
config_bucket = config["bucket"]
config_filename = config["filename"]

if config_project == "" or config_bucket == "" or config_filename == "" :
    print("must specify project, bucket and filename")
    sys.exit(1)

#gcs_client = gcs.Client(project=config_project)
#print(gcs_client)
gcs_client = gcs.Client()
bucket = gcs_client.get_bucket(config_bucket)
print(bucket)
blob = gcs.Blob(config_filename, bucket)

# well, you may exploit the api key and get the season stats as much as you want I guess
r = requests.get('https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/2022?key=f4a3484bae4f42888d12f4cfb3607e08')

result = blob.upload_from_string(r.text)
print("blob upload result", result)

