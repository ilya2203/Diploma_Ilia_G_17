import psycopg2
import credDB
import json
import requests

con = psycopg2.connect(
  database=credDB.database,
  user=credDB.user, 
  password=credDB.password,
  host=credDB.host,
  port=credDB.port
)

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/franchises')
json_content = json.loads(json_response.content)
header_dict = json_content['franchises']

print("Database opened successfully")
cur = con.cursor()
dbName= 'franchises'
cur.execute('''CREATE TABLE IF NOT EXISTS {tableName}
     (franchiseId int PRIMARY KEY NOT NULL,
    mostRecentTeamId int NOT NULL,
    teamName TEXT NOT NULL,
    locationName TEXT NOT NULL)
    ;'''.format(tableName=dbName))
print("Table created successfully")
cur.executemany("""INSERT INTO {tableName}(franchiseId, mostRecentTeamId, teamName, locationName)
VALUES (%(franchiseId)s, %(mostRecentTeamId)s, %(teamName)s, %(locationName)s) ON CONFLICT DO NOTHING""".format(tableName=dbName) , header_dict)
print("Data added successfully")
con.commit()  
con.close()  