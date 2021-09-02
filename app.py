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
def testdb(table_name):
    db_connect=URL.create(dbcred.driver, dbcred.username, dbcred.password, dbcred.host, dbcred.port, dbcred.database)
    db_engine = create_engine(db_connect)
    inspector = inspect(db_engine)
    # Check if table is exist
    if table_name in inspector.get_table_names():
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
    table_name=season
    teams_from_can=[[8],[9],[10],[52],[23],[20],[22]]
    # End static variables 
    # Start DB connection 
    db_connect=URL.create(dbcred.driver, dbcred.username, dbcred.password, dbcred.host, dbcred.port, dbcred.database)
    db_engine = create_engine(db_connect)
    metadata = MetaData()
    # Check if table is exist
    if testdb(season)==True :
        # Drop table if exist
        drop_table = Table(table_name, metadata )
        drop_table.drop(db_engine) 
    # End DB connection
    # Get data about games in season
    url_from_first='https://statsapi.web.nhl.com/api/v1/schedule/?season='+str(season)
    ready_json_first = json.loads(requests.get(url_from_first).content)['dates']
    ready_dict_main = pd.json_normalize(ready_json_first,sep='_')
    games_dates=list(ready_dict_main['date'])
    for game_date in games_dates:
        # Get data about each game_id 
        url_from_second='https://statsapi.web.nhl.com/api/v1/schedule?date='+str(game_date)
        ready_json_second = json.loads(requests.get(url_from_second).content)['dates'][0]['games']
        ready_dict_second = pd.json_normalize(ready_json_second,sep='_')
        games_id=len(list(ready_dict_second['gamePk']))
        for game_id in range(games_id):
            # Get data about teams in all games
            ready_json_third = json.loads(requests.get(url_from_second).content)['dates'][0]['games'][game_id]['teams']['home']['team']
            ready_dict_third = pd.json_normalize(ready_json_third,sep='_')
            ready_json_fourth = json.loads(requests.get(url_from_second).content)['dates'][0]['games'][game_id]['gamePk']
            home_teams_id=list(ready_dict_third['id'])
            # Choose Canadian teams
            if home_teams_id in teams_from_can:
                # Get data about each game in Canada 
                url_from_fifth='https://statsapi.web.nhl.com/api/v1/game/'+str(ready_json_fourth)+'/boxscore'
                ready_json_fifth = json.loads(requests.get(url_from_fifth).content)['teams']
                #print(ready_json_fourth)
                # Get data about players in each game in Canada
                for home_away in ready_json_fifth:
                    #print(home_away)
                    ready_json_sixth = ready_json_fifth[home_away]['players']
                    for player_id in ready_json_sixth:
                        ready_json_seventh = ready_json_sixth[player_id]
                        # Choose nationality
                        if ready_json_seventh['person']['nationality'] == nationality: 
                            # Checking stats field         
                            if len(ready_json_seventh['stats']) == 1: 
                                # Checking keys on field stats         
                                if 'skaterStats' in ready_json_seventh['stats'].keys():
                                    # Checking stats: skaters or goalie and put data in DB
                                    if ready_json_seventh['stats']['skaterStats']['goals'] > 0:
                                        ready_dict_seventh = pd.json_normalize(ready_json_seventh,sep='_')
                                        #print(ready_dict_seventh['person_id'][0])
                                        ready_dict_seventh.to_sql(table_name, db_engine,if_exists='append', index=False)
                                else: 
                                    if ready_json_seventh['stats']['goalieStats']['goals'] > 0:
                                        ready_dict_seventh = pd.json_normalize(ready_json_seventh,sep='_')
                                        #print(ready_dict_seventh['person_id'][0])
                                        ready_dict_seventh.to_sql(table_name, db_engine,if_exists='append', index=False)
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
        FROM {season_table}
        GROUP BY "person_fullName","jerseyNumber","person_currentTeam_name","person_primaryPosition_type"
        ORDER BY SUM DESC
        LIMIT 10
        """.format(season_table=season))
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
    players_db_app=""
    exec_status_app=""
    if request.method == "POST" and request.form.get('getData'):
        if testdb(season)==None :
            get_players(season,nationality)
            exec_status_app="Data execution from API to DB"
        else: exec_status_app="Table already created. Data execution from DB"
        players_db_app=get_players_db('"'+season+'"')
    exec_time_app="%.2f" %(time.time() - start_time)
    return render_template('players.html', exectime=exec_time_app, playersdb=players_db_app, execstatus=exec_status_app)

@app.route('/updatedb',methods=(['GET','POST']))

def updatedb():
    start_time = time.time()
    season='20202021'
    nationality="SWE"
    update_status_app=""
    if request.method == "POST" and request.form.get('update'):
        get_players(season,nationality)
        update_status_app="Table updated up to date"
    exec_time_app="%.2f" %(time.time() - start_time)
    return render_template('updatedb.html', exectime=exec_time_app, updatestatus=update_status_app)

if __name__ == '__main__':
    app.run()