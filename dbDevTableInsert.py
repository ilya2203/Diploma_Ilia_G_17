import psycopg2
import credDB
import jsonDev
from psycopg2.extensions import AsIs

con = psycopg2.connect(
  database=credDB.database,
  user=credDB.user, 
  password=credDB.password,
  host=credDB.host,
  port=credDB.port
)

print("Database opened successfully")
cur = con.cursor()
cur.executemany("""INSERT INTO CONFERENCE(id,name,link,abbreviation,shortName,active) 
VALUES (%(id)s,%(name)s,%(link)s,%(abbreviation)s,%(shortName)s,%(active)s)""", jsonDev.header_dict)
con.commit()  
#print(jsonDev.header_dict)

con.close()  