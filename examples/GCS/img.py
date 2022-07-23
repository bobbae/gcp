# Read data from a URL and store the data into a GCS blob
#
# Download and point to the service account credential file.
# export GOOGLE_APPLICATION_CREDENTIALS=/Users/bob/service-account-1-84f3.json 
#

import argparse
import sys
import requests
from PIL import Image
from google.cloud  import storage as gcs

parser = argparse.ArgumentParser(description="read from URL and store to GCS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-b", "--bucket", default="", help="bucket")
parser.add_argument("-f", "--filename", default="", help="filename")

args = parser.parse_args()
config = vars(args)
print("config",config)

#config_project = config["project"]
config_bucket = config["bucket"]
config_filename = config["filename"]

if config_bucket == "" or config_filename == "" :
    print("must specify bucket and filename")
    sys.exit(1)

gcs_client = gcs.Client()
bucket = gcs_client.get_bucket(config_bucket)
print(bucket)
blob = gcs.Blob("big_"+config_filename, bucket)

img = Image.open(config_filename)
w, h = img.size
print("width", w, "height", h)

newsize = (w * 2, h * 2)
newimg = img.resize(newsize)
newimg_filename = "newimg.jpg"
newimg.save(newimg_filename)

result = blob.upload_from_filename(newimg_filename)
