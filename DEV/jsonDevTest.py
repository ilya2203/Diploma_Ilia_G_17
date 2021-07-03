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
urlFromFirst='https://statsapi.web.nhl.com/api/v1/schedule/?season='+str(season)
readyJsonFirst = json.loads(requests.get(urlFromFirst).content)['dates']
readyDictMain = pd.json_normalize(readyJsonFirst,sep='_')
gamesDates=list(readyDictMain['date'])
for gameDate in gamesDates:
    urlFromSecond='https://statsapi.web.nhl.com/api/v1/schedule?date='+str(gameDate)
    readyJsonSecond = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games']
    readyDictSecond = pd.json_normalize(readyJsonSecond,sep='_')
    gamesId=len(list(readyDictSecond['gamePk']))
    for gameId in range(gamesId):
        readyJsonThird = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games'][gameId]['teams']['home']['team']
        readyDictThird = pd.json_normalize(readyJsonThird,sep='_')
        readyJsonFourth = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games'][gameId]['gamePk']
        homeTeamsId=list(readyDictThird['id'])
        if homeTeamsId in teamsFromCan:
            urlFromFifth='https://statsapi.web.nhl.com/api/v1/game/'+str(readyJsonFourth)+'/boxscore'
            readyJsonFifth = json.loads(requests.get(urlFromFifth).content)['teams']
            print(readyJsonFourth)
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
                                    print(readyDictSeventh)
                            else: 
                                if readyJsonSeventh['stats']['goalieStats']['goals'] > 0:
                                    readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                                    print(readyDictSeventh)
            