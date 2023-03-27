# -*- coding: utf-8 -*-
"""
Python script to load data from csv into DB. 
"""
import psycopg2

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
    data DATE NOT NULL, 
    open FLOAT NOT NULL, 
    high FLOAT NOT NULL, 
    low FLOAT NOT NULL, 
    close FLOAT NOT NULL, 
    adj_close FLOAT NOT NULL, 
    volume BIGINT NOT NULL
                    ); 
"""
cur.execute(create_table_command)


# Read in csv file
'''
market_df = pd.read_csv('MSFT.csv') 
for index, row in market_df.iterrows(): 
    row_open = row['Opemn']'''
    



conn.close()
