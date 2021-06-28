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
cur.execute('''DROP TABLE roster  
     ''')

print("Table droped successfully")
con.commit()  
con.close()