import dbCred # Credential for DB
import psycopg2
# Start DB connection 
con = psycopg2.connect(
database=dbCred.database,
user=dbCred.username, 
password=dbCred.password,
host=dbCred.host,
port=dbCred.port,
)
cur = con.cursor()
cur.execute('''
select "seasonId" 
from seasons 
ORDER BY "seasonId" DESC''')
con.commit()  
rows = cur.fetchall()
con.close()
print(bool(cur.rowcount))
