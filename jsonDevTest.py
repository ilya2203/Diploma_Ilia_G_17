import json
import requests
from requests.models import Response
from requests.sessions import dispatch_hook
#roster start
json_response = requests.get('https://statsapi.web.nhl.com//api/v1/teams/8/roster')
json_content = json.loads(json_response.content)
header_dict = json_content['roster'][0]['person']
print(header_dict.keys())
print(header_dict.items())
temp=[]
dicklsit=[]
for person in header_dict.items():
    temp=[person]
    dicklsit.append(temp)
print(dicklsit)
dicklsit
print(dicklsit.keys())





#print(json.dumps(json_content['roster'][0]['person'], indent = 4, sort_keys=True))
