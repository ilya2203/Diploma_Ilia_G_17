import json 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df
import requests

#load json object
json_response = requests.get('https://statsapi.web.nhl.com//api/v1/teams/8/roster')
json_data = json.loads(json_response.content)

roster = pd.json_normalize(json_data['roster'],sep='_')
for x in roster:
    print(x)

#print(roster.keys())