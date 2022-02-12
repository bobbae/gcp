import requests
from google.cloud  import storage as gcs

r = requests.get('https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/2022?key=fffffffffffffffffff')

#print(r.text)

gcs_client = gcs.Client(project='xxx-project-123')
bucket = gcs_client.get_bucket('bob-test-bucket-123')
blob = gcs.Blob('file1.txt', bucket)
blob.upload_from_string(r.text)
