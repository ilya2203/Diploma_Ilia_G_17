import psycopg2
import credDB

con = psycopg2.connect(
  database=credDB.database,
  user=credDB.user, 
  password=credDB.password,
  host=credDB.host,
  port=credDB.port
)

print("Database opened successfully")
cur = con.cursor()  
DEVTEAMS= 'TEAMS'
cur.execute('''CREATE TABLE IF NOT EXISTS {tab}
     (id int PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    active BOOLEAN NOT NULL)
    ;'''.format(tab=DEVTEAMS))

print("Table created successfully")
con.commit()  
con.close()