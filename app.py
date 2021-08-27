from flask import Flask, render_template, request
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
from sqlalchemy import MetaData # Module for MetaData
from sqlalchemy import Table # Module for work with table
from sqlalchemy.inspection import inspect # Module for view tables
import time # Import time
import dbcred # Credential for DB
import json # Json module
import requests # Module for URL request
import pandas as pd # Module for JSON arrange
import psycopg2
##-> Start Information about function testdb
# Checking if table exist
##<- End Information about function
###-> Start of function testdb 
def testdb(tableName):
    dbConnect=URL.create(dbcred.driver, dbcred.username, dbcred.password, dbcred.host, dbcred.port, dbcred.database)
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
    tablename=season
    teamsfromcan=[[8],[9],[10],[52],[23],[20],[22]]
    # End static variables 
    # Start DB connection 
    dbconnect=URL.create(dbcred.driver, dbcred.username, dbcred.password, dbcred.host, dbcred.port, dbcred.database)
    dbengine = create_engine(dbconnect)
    metadata = MetaData()
    inspector = inspect(dbengine)
    # Check if table is exist
    if testdb(season)==True :
        # Drop table if exist
        droptable = Table(tablename, metadata )
        droptable.drop(dbengine) 
    # End DB connection
    # Get data about games in season
    urlfromfirst='https://statsapi.web.nhl.com/api/v1/schedule/?season='+str(season)
    readyjsonfirst = json.loads(requests.get(urlfromfirst).content)['dates']
    readydictmain = pd.json_normalize(readyjsonfirst,sep='_')
    gamesdates=list(readydictmain['date'])
    for gamedate in gamesdates:
        # Get data about each gameID 
        urlfromsecond='https://statsapi.web.nhl.com/api/v1/schedule?date='+str(gamedate)
        readyjsonsecond = json.loads(requests.get(urlfromsecond).content)['dates'][0]['games']
        readydictsecond = pd.json_normalize(readyjsonsecond,sep='_')
        gamesid=len(list(readydictsecond['gamePk']))
        for gameid in range(gamesid):
            # Get data about teams in all games
            readyjsonthird = json.loads(requests.get(urlfromsecond).content)['dates'][0]['games'][gameid]['teams']['home']['team']
            readydictthird = pd.json_normalize(readyjsonthird,sep='_')
            readyjsonfourth = json.loads(requests.get(urlfromsecond).content)['dates'][0]['games'][gameid]['gamePk']
            hometeamsid=list(readydictthird['id'])
            # Choose Canadian teams
            if hometeamsid in teamsfromcan:
                # Get data about each game in Canada 
                urlfromfifth='https://statsapi.web.nhl.com/api/v1/game/'+str(readyjsonfourth)+'/boxscore'
                readyjsonfifth = json.loads(requests.get(urlfromfifth).content)['teams']
                #print(readyJsonFourth)
                # Get data about players in each game in Canada
                for homeaway in readyjsonfifth:
                    #print(homeAway)
                    readyjsonsixth = readyjsonfifth[homeaway]['players']
                    for playerid in readyjsonsixth:
                        readyjsonseventh = readyjsonsixth[playerid]
                        # Choose nationality
                        if readyjsonseventh['person']['nationality'] == nationality: 
                            # Checking stats field         
                            if len(readyjsonseventh['stats']) == 1: 
                                # Checking keys on field stats         
                                if 'skaterStats' in readyjsonseventh['stats'].keys():
                                    # Checking stats: skaters or goalie and put data in DB
                                    if readyjsonseventh['stats']['skaterStats']['goals'] > 0:
                                        readydictseventh = pd.json_normalize(readyjsonseventh,sep='_')
                                        #print(readyDictSeventh['person_id'][0])
                                        readydictseventh.to_sql(tablename, dbengine,if_exists='append', index=False)
                                else: 
                                    if readyjsonseventh['stats']['goalieStats']['goals'] > 0:
                                        readydictseventh = pd.json_normalize(readyjsonseventh,sep='_')
                                        #print(readyDictSeventh['person_id'][0])
                                        readydictseventh.to_sql(tablename, dbengine,if_exists='append', index=False)
###<- End of function Get_players with 2 variables

##-> Start Information about function get_players_db
# Check connect to table and get players
##<- End Information about function get_players_db
def dbconnecting():
    con = psycopg2.connect(
    database=dbcred.database,
    user=dbcred.username, 
    password=dbcred.password,
    host=dbcred.host,
    port=dbcred.port,
    )
    return con
###-> Start of function get_players_db
def get_players_db(season):
    con = dbconnecting()
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
    playersdbapp=""
    execstatusapp=""
    if request.method == "POST" and request.form.get('getData'):
        if testdb(season)==None :
            get_players(season,nationality)
            execstatusapp="Data execution from API to DB"
        else: execstatusapp="Table already created. Data execution from DB"
        playersdbapp=get_players_db('"'+season+'"')
    exectimeapp="%.2f" %(time.time() - start_time)
    return render_template('players.html', exectime=exectimeapp, playersdb=playersdbapp, execstatus=execstatusapp)

@app.route('/updatedb',methods=(['GET','POST']))

def updatedb():
    start_time = time.time()
    season='20202021'
    nationality="SWE"
    updatestatusapp=""
    if request.method == "POST" and request.form.get('update'):
        get_players(season,nationality)
        updatestatusapp="Table updated up to date"
    exectimeapp="%.2f" %(time.time() - start_time)
    return render_template('updatedb.html', exectime=exectimeapp, updatestatus=updatestatusapp)

if __name__ == '__main__':
    app.run()