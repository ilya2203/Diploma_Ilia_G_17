import dbCred # Credential for DB
import json
import requests
import pandas as pd # Module for JSON arrange
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy import * # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
# Start variable list
tableName='sweden'
season='20202021'
teamsFromCan=[[8],[9],[10],[52],[23],[20],[22]]
nationality='SWE'
# End varibale list
# Start DB connection 
dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
dbEngine = create_engine(dbConnect)
metadata = MetaData() 
# End DB connection
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
                                    print(readyDictSeventh['person_id'][0])
                                    readyDictSeventh.to_sql(tableName, dbEngine,if_exists='append', index=False)
                            else: 
                                if readyJsonSeventh['stats']['goalieStats']['goals'] > 0:
                                    readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                                    print(readyDictSeventh['person_id'][0])
                                    readyDictSeventh.to_sql(tableName, dbEngine,if_exists='append', index=False)




#readyDictThird.to_sql(tableName, dbEngine,if_exists='append', index=False)



