import dbCred # Credential for DB
import psycopg2
# Start of function dbConnecting
def dbConnecting():
    con = psycopg2.connect(
    database=dbCred.database,
    user=dbCred.username, 
    password=dbCred.password,
    host=dbCred.host,
    port=dbCred.port,
    )
    return con
# End of function dbConnecting
# Start of function get_players_db
def get_players_db():
    con = dbConnecting()
    cur = con.cursor()
    cur.execute("""
        SELECT "person_fullName","jerseyNumber","person_currentTeam_name","person_primaryPosition_type",
        SUM("stats_skaterStats_goals")
        FROM Players
        GROUP BY "person_fullName","jerseyNumber","person_currentTeam_name","person_primaryPosition_type"
        ORDER BY SUM DESC
        LIMIT 10
        """)
    con.commit()  
    rows = cur.fetchall()
    con.close()
    return rows
# End of function get_players_db
# Start of function get_seasons_db
def get_seasons_db():
    con = dbConnecting()
    cur = con.cursor()
    cur.execute('''
    select "seasonId" 
    from seasons 
    ORDER BY "seasonId" DESC''')
    con.commit()  
    rows = cur.fetchall()
    con.close()
    return rows
# End of function get_seasons_db
