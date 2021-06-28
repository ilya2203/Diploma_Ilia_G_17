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
cur.execute("SELECT * from CONFERENCE")
  
rows = cur.fetchall()
#print(rows)
for row in rows:  
   print("id =", row[0])
   print("NAME =", row[1])
   print("LINK =", row[2])
   print("ABBREVIATION =", row[3])
   print("SHORTNAME =", row[4])
   print("ACTIVE =", row[5], "\n")

print("Operation done successfully")  
con.close()  