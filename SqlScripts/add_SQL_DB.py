import pandas as pd
from sqlalchemy import create_engine


user = 'root'
password = 'root'
host = 'localhost'
port = 10101
database = 'elections_benchmark'

connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)
excel_file = '../electionFrance.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet1')  # Adjust sheet_name as needed

table_name = 'elections'
df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

print(f"Data imported successfully into {table_name} table.")