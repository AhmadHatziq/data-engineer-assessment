# -*- coding: utf-8 -*-
"""
Python script to load data from csv into DB. 
"""
import psycopg2

# Connect to postgres. 
conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=password")
conn.set_session(autocommit=True)
cur = conn.cursor()
conn.close()
