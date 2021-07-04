import dbCred # Credential for DB
import json # Json module
import requests # Module for URL request
import pandas as pd # Module for JSON arrange
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy import * # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
from sqlalchemy.engine.reflection import Inspector # Module for view tables
# Start of function Get_players with 2 variables
def get_seasons():
    # Start static variables 
    tableName='seasons'
    # End static variables 
    # Start DB connection 
    dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
    dbEngine = create_engine(dbConnect)
    metadata = MetaData()
    inspector = inspect(dbEngine)
    # Check if table is exist
    if tableName in inspector.get_table_names() == True:
        # Drop table if exist
        dropTable = Table(tableName, metadata )
        dropTable.drop(dbEngine) 
    # End DB connection
    # Get data about games in season
    urlFromFirst='https://statsapi.web.nhl.com/api/v1/seasons'
    readyJsonFirst = json.loads(requests.get(urlFromFirst).content)['seasons']
    readyDictMain = pd.json_normalize(readyJsonFirst,sep='_')
    readyDictMain.to_sql(tableName, dbEngine,if_exists='replace', index=False)
# End of function Get_players with 2 variables

get_seasons()