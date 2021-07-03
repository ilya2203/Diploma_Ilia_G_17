import json 
import pandas as pd 
from pandas.io.json import json_normalize # Package for flattening json in pandas df
import requests
# Variable
readyJsonFourth='2020020004'
nationality='SWE'
urlFromFifth='https://statsapi.web.nhl.com/api/v1/game/'+str(readyJsonFourth)+'/boxscore'
readyJsonFifth = json.loads(requests.get(urlFromFifth).content)['teams']
for homeAway in readyJsonFifth:
    print(homeAway)
    readyJsonSixth = readyJsonFifth[homeAway]['players']
    for playerId in readyJsonSixth:
        readyJsonSeventh = readyJsonSixth[playerId]
        if readyJsonSeventh['person']['nationality'] == nationality:
            if len(readyJsonSeventh['stats']) == 1:          
                if 'skaterStats' in readyJsonSeventh['stats'].keys():
                    if readyJsonSeventh['stats']['skaterStats']['goals'] > 0:
                        readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                        print(readyDictSeventh['person_id'][0])
                else: 
                    if readyJsonSeventh['stats']['goalieStats']['goals'] > 0:
                        readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                        print(readyDictSeventh['person_id'][0])
            

        
   

