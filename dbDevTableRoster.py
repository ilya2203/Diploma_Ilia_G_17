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

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/8/roster')
json_content = json.loads(json_response.content)
header_dict = json_content['roster']
print(header_dict)
print("Database opened successfully")
cur = con.cursor()
dbName= 'roster'
cur.execute('''CREATE TABLE IF NOT EXISTS {tableName}
    (id int PRIMARY KEY NOT NULL,
    fullName TEXT ,
    link TEXT )
    ;'''.format(tableName=dbName))
print("Table created successfully")
cur.executemany("""INSERT INTO {tableName}(id) 
VALUES (%(id)s) ON CONFLICT DO NOTHING""".format(tableName=dbName) ,header_dict)

print("Data added successfully")
con.commit()  
con.close()  