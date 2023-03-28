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
drop_table_command = "DROP TABLE IF EXISTS daily_stock;"
cur.execute(drop_table_command)

# Create table. 
create_table_command = """
CREATE TABLE IF NOT EXISTS msft_stock (
    id SERIAL PRIMARY KEY, 
    stock_symbol VARCHAR(10) NOT NULL, 
    date DATE NOT NULL, 
    open FLOAT NOT NULL, 
    high FLOAT NOT NULL, 
    low FLOAT NOT NULL, 
    close FLOAT NOT NULL, 
    adj_close FLOAT NOT NULL, 
    volume BIGINT NOT NULL
                    ); 
"""
cur.execute(create_table_command)

# Define insert statement 
msft_stock_table_insert = (""" 
INSERT INTO msft_stock (stock_symbol, date, open, high, low, close, adj_close, volume) 
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s) 
""")


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
    cur.execute(msft_stock_table_insert, row_data)


# Close connection to DB. 
conn.close()
