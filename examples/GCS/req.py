# Read data from a URL and store the data into a GCS blob

import requests
from google.cloud  import storage as gcs

r = requests.get('https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/2022?key=f4a3484bae4f42888d12f4cfb3607e08')

#print(r.text)

gcs_client = gcs.Client(project='sada-u-4')
bucket = gcs_client.get_bucket('bob-test123')
blob = gcs.Blob('file1.txt', bucket)
blob.upload_from_string(r.text)
