import pandas as pd
import couchdb

couchdb_url = 'http://localhost:11210/'
database_name = 'elections-couchdb'
username = 'admin'
password = 'password'

try:
    # Connect to CouchDB server
    couch = couchdb.Server(couchdb_url)
    couch.resource.credentials = (username , password)
    # Create a new database or connect to an existing one
    if database_name in couch:
        db = couch[database_name]
        print(f"Connected to existing database: {database_name}")
    else:
        db = couch.create(database_name)
        print(f"Created new database: {database_name}")

    # Read the Excel file
    excel_file = '../electionFrance.xlsx'
    df = pd.read_excel(excel_file, sheet_name='Sheet1')  # Adjust sheet_name as needed
    docs = []
    # Insert the DataFrame rows into CouchDB
    for _, row in df.iterrows():
        doc = row.to_dict()
        docs.append(doc)
    db.update(docs)


    print(f"Data imported successfully into {database_name} database.")

except Exception as e:
    print(f"An error occurred: {e}")