from flask import Flask, render_template, request
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
from sqlalchemy import MetaData # Module for MetaData
from sqlalchemy import Table # Module for work with table
from sqlalchemy.inspection import inspect # Module for view tables
import time # Import time
import dbCred # Credential for DB
import json # Json module
import requests # Module for URL request
import pandas as pd # Module for JSON arrange
import psycopg2
##-> Start Information about function testDB
# Checking if table exist
##<- End Information about function
###-> Start of function testDB 
def testDB(tableName):
    dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
    dbEngine = create_engine(dbConnect)
    inspector = inspect(dbEngine)
    # Check if table is exist
    if tableName in inspector.get_table_names():
        return True
###<- End of function testDB

##-> Start Information about function
# for example:
# nationality='SWE'
# season='20202021'
# get_players('20202021','SWE')
##<- End Information about function
###-> Start of function get_players with 2 variables
def get_players(season,nationality):
    # Start static variables 
    tableName=season
    teamsFromCan=[[8],[9],[10],[52],[23],[20],[22]]
    # End static variables 
    # Start DB connection 
    dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
    dbEngine = create_engine(dbConnect)
    metadata = MetaData()
    inspector = inspect(dbEngine)
    # Check if table is exist
    if testDB==True :
        # Drop table if exist
        dropTable = Table(tableName, metadata )
        dropTable.drop(dbEngine) 
    # End DB connection
    # Get data about games in season
    urlFromFirst='https://statsapi.web.nhl.com/api/v1/schedule/?season='+str(season)
    readyJsonFirst = json.loads(requests.get(urlFromFirst).content)['dates']
    readyDictMain = pd.json_normalize(readyJsonFirst,sep='_')
    gamesDates=list(readyDictMain['date'])
    for gameDate in gamesDates:
        # Get data about each gameID 
        urlFromSecond='https://statsapi.web.nhl.com/api/v1/schedule?date='+str(gameDate)
        readyJsonSecond = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games']
        readyDictSecond = pd.json_normalize(readyJsonSecond,sep='_')
        gamesId=len(list(readyDictSecond['gamePk']))
        for gameId in range(gamesId):
            # Get data about teams in all games
            readyJsonThird = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games'][gameId]['teams']['home']['team']
            readyDictThird = pd.json_normalize(readyJsonThird,sep='_')
            readyJsonFourth = json.loads(requests.get(urlFromSecond).content)['dates'][0]['games'][gameId]['gamePk']
            homeTeamsId=list(readyDictThird['id'])
            # Choose Canadian teams
            if homeTeamsId in teamsFromCan:
                # Get data about each game in Canada 
                urlFromFifth='https://statsapi.web.nhl.com/api/v1/game/'+str(readyJsonFourth)+'/boxscore'
                readyJsonFifth = json.loads(requests.get(urlFromFifth).content)['teams']
                #print(readyJsonFourth)
                # Get data about players in each game in Canada
                for homeAway in readyJsonFifth:
                    #print(homeAway)
                    readyJsonSixth = readyJsonFifth[homeAway]['players']
                    for playerId in readyJsonSixth:
                        readyJsonSeventh = readyJsonSixth[playerId]
                        # Choose nationality
                        if readyJsonSeventh['person']['nationality'] == nationality: 
                            # Checking stats field         
                            if len(readyJsonSeventh['stats']) == 1: 
                                # Checking keys on field stats         
                                if 'skaterStats' in readyJsonSeventh['stats'].keys():
                                    # Checking stats: skaters or goalie and put data in DB
                                    if readyJsonSeventh['stats']['skaterStats']['goals'] > 0:
                                        readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                                        #print(readyDictSeventh['person_id'][0])
                                        readyDictSeventh.to_sql(tableName, dbEngine,if_exists='append', index=False)
                                else: 
                                    if readyJsonSeventh['stats']['goalieStats']['goals'] > 0:
                                        readyDictSeventh = pd.json_normalize(readyJsonSeventh,sep='_')
                                        #print(readyDictSeventh['person_id'][0])
                                        readyDictSeventh.to_sql(tableName, dbEngine,if_exists='append', index=False)
###<- End of function Get_players with 2 variables

##-> Start Information about function get_players_db
# Check connect to table and get players
##<- End Information about function get_players_db
def dbConnecting():
    con = psycopg2.connect(
    database=dbCred.database,
    user=dbCred.username, 
    password=dbCred.password,
    host=dbCred.host,
    port=dbCred.port,
    )
    return con
###-> Start of function get_players_db
def get_players_db(season):
    con = dbConnecting()
    cur = con.cursor()
    cur.execute("""
        SELECT "person_fullName","jerseyNumber","person_currentTeam_name","person_primaryPosition_type",
        SUM("stats_skaterStats_goals")
        FROM {seasonTable}
        GROUP BY "person_fullName","jerseyNumber","person_currentTeam_name","person_primaryPosition_type"
        ORDER BY SUM DESC
        LIMIT 10
        """.format(seasonTable=season))
    con.commit()  
    rows = cur.fetchall()
    con.close()
    return rows
###<- End of function get_players_db

#-> for applications
app = Flask(__name__)

@app.route('/',methods=(['GET']))
def index():
    return render_template('index.html')

@app.route('/players',methods=(['GET','POST']))

def players():
    start_time = time.time()
    season='20202021'
    nationality="SWE"
    playersDbApp=""
    if request.method == "POST" and request.form.get('getData'):
        get_players(season,nationality)
        playersDbApp=get_players_db('"'+season+'"')
    execTimeApp="%.2f" %(time.time() - start_time)
    return render_template('players.html', execTime=execTimeApp, playersDb=playersDbApp)

if __name__ == '__main__':
    app.run(debug=True)