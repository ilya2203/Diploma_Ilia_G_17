import credDB # Credential for DB
import json
import requests
import psycopg2
from psycopg2.extensions import AsIs
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df

con = psycopg2.connect(
    database=credDB.database,
    user=credDB.user, 
    password=credDB.password,
    host=credDB.host,
    port=credDB.port
  )

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/8/roster')
json_content = json.loads(json_response.content)
header_dict = json_content['roster']
roster = pd.json_normalize(header_dict,sep='_')
print("Database opened successfully")
cur = con.cursor()
dbName= 'roster'
cur.execute('''DROP TABLE IF EXISTS roster''')
cur.execute('''CREATE TABLE IF NOT EXISTS {tableName}
    (person_id int PRIMARY KEY NOT NULL,
    person_fullName TEXT NOT NULL,
    person_link text NOT NULL,
    jerseyNumber int NOT NULL,
    position_code text NOT NULL,
    position_name text NOT NULL,
    position_type text NOT NULL,
    position_abbreviation text NOT NULL)
    ;'''.format(tableName=dbName))
print("Table created successfully")
# Create a list of tupples from the dataframe values
tuples = [tuple(x) for x in roster.to_numpy()]
    # Comma-separated dataframe columns
cols = ','.join(list(roster.columns))
    # SQL quert to execute
query  = "INSERT INTO %s (%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % (dbName, cols)
cursor = con.cursor()

cursor.executemany(query, tuples)
print("All Rosters added")
con.commit()  
con.close()  