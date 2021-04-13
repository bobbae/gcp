#
# 1. get a list of projects
# 2. get iam policy for each proj
# 3. find project that has roles/owner and print it
import subprocess
import json

projects = subprocess.Popen(['gcloud', 'projects', 'list', '--format=json'], stdout=subprocess.PIPE).communicate()[0]

projects2 =  json.loads(projects.decode('utf-8').replace('\n', ' '))

for proj in projects2:
    projid = proj['projectId']
    try:
        iamp = subprocess.Popen(['gcloud', 'projects', 'get-iam-policy', projid, '--format=json'], stdout=subprocess.PIPE).communicate()[0]
        iamp2 = json.loads(iamp.decode('utf-8').replace('\n', ' '))
        for b in iamp2['bindings']:
            role=b['role']
            if role=='roles/owner':
                print(projid,'owner')
    except:
        pass
