# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:16:42 2023
Prints the output of a specified SQL query given the input file. 
@author: hatzi
"""

import sys
import psycopg2

if len(sys.argv) != 2:
    print("Usage: python run_sql_query.py [sql_command_file]")
    sys.exit(1)

# Get file input from the user. 
sql_file = sys.argv[1]

# Read in the SQL command contents. 
with open(sql_file, 'r') as sql_statement_file: 
    sql_command = sql_statement_file.read()
    
# Connect to postgres. 
conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=password")
conn.set_session(autocommit=True)
cur = conn.cursor()

# Execute command. 
cur.execute(sql_command)

# Print the results to the console. 
col_names = [desc[0] for desc in cur.description]
rows = cur.fetchall()
print('\t'.join(col_names))
for row in rows:
    print('\t'.join(str(x) for x in row))

