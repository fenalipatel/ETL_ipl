import os
import pandas as pd
from sqlalchemy import create_engine

def create_connection():
    connection = None
    try:
        connection = create_engine(
            'mysql+mysqlconnector://root:my-secret-pw@localhost/pydb'
        )
        print('Connected to MySQL database')
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")

    return connection

def insert_csv_data(connection, csv_file):
    try:
        df = pd.read_csv(csv_file)
        table_name = "ipl_match_2007_2023_table"
        df.to_sql(table_name, connection, if_exists='append', index=False)
        print(f"Data from {csv_file} inserted into MySQL table '{table_name}'")
    except Exception as e:
        print(f"Error inserting data from {csv_file} into MySQL: {e}")

def process_csv_files(connection, directory):
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                csv_file = os.path.join(directory, filename)
                insert_csv_data(connection, csv_file)
    except Exception as e:
        print(f"Error processing CSV files: {e}")

connection = create_connection()
if connection:
    directory = "C:/Users/JAY/OneDrive/Desktop/internship/repo/ETL_ipl/processed_files"
    process_csv_files(connection, directory)
    connection.dispose()
