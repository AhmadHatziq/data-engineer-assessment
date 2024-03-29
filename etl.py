# -*- coding: utf-8 -*-
"""
Python script to load data from csv into DB. 
"""
import psycopg2
import pandas as pd 

# Connect to postgres. 
conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=password")
conn.set_session(autocommit=True)
cur = conn.cursor()

# Drop table if it already exists. 
drop_table_command = "DROP TABLE IF EXISTS msft_stock;"
cur.execute(drop_table_command)

# Run CREATE TABLE command. 
with open('create_table.txt', 'r') as create_table_file: 
    create_table_command = create_table_file.read()
cur.execute(create_table_command)

# Define insert statement 
with open('insert_row.txt', 'r') as insert_row_file: 
    insert_command = insert_row_file.read()

# Read in csv file
market_df = pd.read_csv('MSFT.csv')

# Iterate over each row
for index, row in market_df.iterrows(): 
    
    # Extract values 
    date_string = row['Date'],
    open_string = row['Open'],
    high_string = row['High'],
    low_string = row['Low'],
    close_string = row['Close'],
    adj_close_string = row['Adj Close'],
    volume_string = row['Volume']  
    
    # Store values into a single list 
    row_data = ['MSFT', date_string, open_string, high_string, low_string, 
                close_string, adj_close_string, volume_string]
    
    # Store into DB 
    cur.execute(insert_command, row_data)

# Sanity check: Check that the number of rows in the DB and CSV matches. 
print('CSV length: ', len(market_df))
cur.execute("SELECT COUNT(*) FROM msft_stock;")
table_length = cur.fetchone()[0]
print('Table length: ', table_length)

if table_length != len(market_df): 
    print('Unequal values ingested.')

# Close connection to DB. 
conn.close()
print("Ingesting complete.")