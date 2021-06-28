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

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
json_content = json.loads(json_response.content)
header_dict = json_content['teams']
print("Database opened successfully")
cur = con.cursor()
dbName= 'TEAMS'
cur.execute('''CREATE TABLE IF NOT EXISTS {tableName}
     (id int PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    locationName TEXT NOT NULL,
    franchiseId int NOT NULL,
    active BOOLEAN NOT NULL)
    ;'''.format(tableName=dbName))
print("Table created successfully")
cur.executemany("""INSERT INTO {tableName}(id, name, locationName, franchiseId, active) 
VALUES (%(id)s, %(name)s, %(locationName)s, %(franchiseId)s, %(active)s) ON CONFLICT DO NOTHING""".format(tableName=dbName) , header_dict)
print("Data added successfully")
con.commit()  
con.close()  