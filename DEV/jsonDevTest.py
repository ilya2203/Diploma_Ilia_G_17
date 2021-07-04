import json 
import pandas as pd 
from pandas.io.json import json_normalize # Package for flattening json in pandas df
import requests
# Start variable list
season='20202021'
teamsFromCan=[[8],[9],[10],[52],[23],[20],[22]]
nationality='SWE'
# End varibale list
# Start ot application
urlFromFirst='https://statsapi.web.nhl.com/api/v1/seasons'
readyJsonFirst = json.loads(requests.get(urlFromFirst).content)
readyDictMain = pd.json_normalize(readyJsonFirst,sep='_')['seasons']
print(readyDictMain)
