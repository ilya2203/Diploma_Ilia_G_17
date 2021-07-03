import dbCred # Credential for DB
import json
import requests
import pandas as pd # Module for JSON arrange
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy import * # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
# Variable
season='20202021'
tableName='rosters'
# DB connection 
dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
dbEngine = create_engine(dbConnect)
metadata = MetaData() 
# dropTable = Table(tableName, metadata ) # defines the table structure in the 'python' schema of our connection to the db
# dropTable.drop(dbEngine)
# Receive teams ID from API
urlFromMain='https://statsapi.web.nhl.com/api/v1/teams/'
readyJsonMain = json.loads(requests.get(urlFromMain).content)['teams']
readyDictMain = pd.json_normalize(readyJsonMain,sep='_')
teamsId=list(readyDictMain['id'])
for teamId in teamsId:
    urlFromSecond='https://statsapi.web.nhl.com/api/v1/teams/'+str(teamId)+'?expand=team.roster&season='+str(season)
    readyJsonSecond = json.loads(requests.get(urlFromSecond).content)['teams'][0]['roster']['roster']
    readyDictSecond = pd.json_normalize(readyJsonSecond,sep='_')
    playersId=list(readyDictSecond['person_id'])
    for playerId in playersId:
        #Receive players data from API and put into DB
        urlFromThird='https://statsapi.web.nhl.com/api/v1/people/'+str(playerId)
        readyJsonThird = json.loads(requests.get(urlFromThird).content)['people']
        readyDictThird = pd.json_normalize(readyJsonThird,sep='_')
        readyDictThird.to_sql(tableName, dbEngine,if_exists='append', index=False)



