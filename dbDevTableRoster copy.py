import psycopg2
import credDB
import json
import requests
from psycopg2.extensions import AsIs

con = psycopg2.connect(
  database=credDB.database,
  user=credDB.user, 
  password=credDB.password,
  host=credDB.host,
  port=credDB.port
)

json_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/8/roster')
json_content = json.loads(json_response.content)
header_dict = json_content['roster'][0]['person']
print(header_dict)
print("Database opened successfully")
cur = con.cursor()
dbName= 'roster'
cur.execute('''CREATE TABLE IF NOT EXISTS {tableName}
    (id int PRIMARY KEY NOT NULL,
    fullName TEXT NOT NULL,
    link text)
    ;'''.format(tableName=dbName))
print("Table created successfully")
columns = header_dict.keys()
values = [header_dict[column] for column in columns]
#insert_statement = 'insert into roster (%s) values %s '
#cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
cur.execute("""INSERT INTO {tableName} (%s) VALUES %s ON CONFLICT DO NOTHING""".format(tableName=dbName), (AsIs(','.join(columns)), tuple(values)))
print("Data added successfully")
con.commit()  
con.close()  