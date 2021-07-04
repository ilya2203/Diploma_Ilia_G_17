import dbCred # Credential for DB
import json
import requests
import pandas as pd # Module for JSON arrange
from sqlalchemy import create_engine # Module for working with DB
from sqlalchemy import * # Module for working with DB
from sqlalchemy.engine.url import URL # Module for working with DB
from sqlalchemy.engine.reflection import Inspector
# Start variable list
tableName='sweden'
season='20202021'
teamsFromCan=[[8],[9],[10],[52],[23],[20],[22]]
nationality='SWE'
# End varibale list
# Start DB connection 
dbConnect=URL.create(dbCred.driver, dbCred.username, dbCred.password, dbCred.host, dbCred.port, dbCred.database)
dbEngine = create_engine(dbConnect)
metadata = MetaData()
inspector = inspect(dbEngine)
# Check if table is exist
if tableName in inspector.get_table_names() ==True:
    # Drop table if exist
    dropTable = Table(tableName, metadata )
    dropTable.drop(dbEngine)


# End DB connection
# Start ot application

