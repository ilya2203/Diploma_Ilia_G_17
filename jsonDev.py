import json
import requests

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/conferences')
json_content = json.loads(json_response.content)

# navigate the json, which are nested lists of dicts
# this below gives you the first, and only, header-dict
header_dict = json_content['conferences']
print(header_dict)