import json
import requests
from requests.models import Response
from requests.sessions import dispatch_hook
#roster start
json_response = requests.get('https://statsapi.web.nhl.com//api/v1/teams/8/roster')
json_content = json.loads(json_response.content)
header_dict = json_content['roster']
#print(header_dict.keys())
for roster in header_dict:
    personColumns = roster['person'].keys()
    personValues = [roster['person'] for column in personColumns]
    positionColumns = roster['position'].keys()
    positionValues = [roster['position'] for column in positionColumns]
    #print(personColumns)
    #print(positionColumns)
  
    all= roster['person']|roster['position']
    columns=all.keys()
    values=[all for column in columns]

print()
print(header_dict)


    






#print(json.dumps(json_content['roster'][0]['person'], indent = 4, sort_keys=True))
