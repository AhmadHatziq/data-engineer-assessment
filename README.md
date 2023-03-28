# data-engineer-assessment

# Table of Contents
1. [Database Schema](#example)
2. [Calculating Aggregated Summaries](#calculating-aggregated-summaries)
3. [System Design](#system-design)

# Setup 
For the assignment, I have created a POSTGRES database and hardcoded the database credentials into my code. 
There is a Python script (`etl.py`) which will create the table, read in the csv file and load the data into the table.
Additionally, the Python script require the `pandas` and `psycopg2` libraries. 

# Folder Contents
- `etl.py` - Python script to create the table and load data from the csv file. 
- `MSFT.csv` - Data file. 
- `create_table.txt` - SQL CREATE table command. 
- `insert_row.txt` - SQL INSERT command. 
- `monthly_average.txt` - SQL command to obtain monthly average. 
- `weekly_average.txt` - SQL command to obtain weekly average.  
- `quarterly_average.txt` - SQL command to obtain quarterly average.  
- `yearly_average.txt` - SQL command to obtain yearly average.  
- `run_sql_query.py` - Python script that can be used to run the SQL commands. 

# Database Schema 
The table schema is as follows: 
- stock_symbol - VARCHAR(10)
- date - DATE 
- open - FLOAT 
- high - FLOAT
- low - FLOAT 
- close - FLOAT 
- adj_close - FLOAT
- volume - BIGINT 

The CREATE TABLE statement is as follows: 
```
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
```

# ETL Script 
To import data into the table, the script `etl.py` will CREATE the table and insert the information using Python. 

The expected usage is as follows: 
```
> python etl.py
CSV length:  1259
Table length:  1259
Ingesting complete.
```

Additionally, there is a sanity check on the total rows ingested. 

# Calculating Aggregated Summaries
To find the weekly, monthly, quarterly and yearly summaries, the SQL commands can be found in the following files: 
- `weekly_average.txt`, `monthly_average.txt`, `quarterly_average.txt` and `yearly_average.txt`

There is a helper script, which can be used to run the SQL commands and output the results. 
The sample usage is as follows: 

`python run_sql_query.py quarterly_average.txt`

Output: 
```
year    quarter average_high            average_low              average_volume
2017    1       65.03892864285714       64.37142885714286       21058700.000000000000
2017    2       69.0282536984127        68.13396785714285       25081373.015873015873
```

The SQL commands can be found below as well. 
## Weekly Average
```
SELECT 
  EXTRACT(WEEK FROM date) AS week,
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(YEAR FROM date) AS year,
  AVG(high) AS average_high_weekly,
  AVG(low) AS average_low_weekly,
  AVG(volume) AS average_volume_weekly
FROM
  msft_stock
GROUP BY
  year,
  month, 
  week
ORDER BY
  year,
  month, 
  week;
```

## Monthly Average
```
SELECT 
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(YEAR FROM date) AS year,
  AVG(high) AS average_high_weekly,
  AVG(low) AS average_low_weekly,
  AVG(volume) AS average_volume_weekly
FROM
  msft_stock
GROUP BY
  year,
  month
ORDER BY
  year,
  month;
```

## Quarterly Average
```
SELECT 
  EXTRACT(YEAR FROM date) AS year,
  CEIL(EXTRACT(MONTH FROM date) / 3.0) AS quarter,
  AVG(high) AS average_high,
  AVG(low) AS average_low,
  AVG(volume) AS average_volume
FROM
  msft_stock
GROUP BY
  year, quarter
ORDER BY
  year, quarter; 
```

## Yearly Average
```
SELECT 
  EXTRACT(YEAR FROM date) AS year,
  AVG(high) AS average_high_weekly,
  AVG(low) AS average_low_weekly,
  AVG(volume) AS average_volume_weekly
FROM
  msft_stock
GROUP BY
  year
ORDER BY
  year; 
```

# System Design
The pipeline architecture will consist of 4 stages: 
1. Data Ingestion 
2. Stream Processing 
3. Data Storage 
4. API

## 1. Data Ingestion 
This stage involves ingesting the data from the source. 

Below are the assumptions we make: 
1. Data is properly formatted. All the stock data has the same format and there is an assured data quality. There is minimal or no missing data points. 
2. Data for each stock is sent at regular intervals. The data for each stock can be sent via a regular stream. 

Possible options: 
- Apache Kafka
- Amazon Kinesis 

Discussion: 
Amazon Kinesis would be ideal if the customer is also using other AWS services. By using Kinesis, we can also leverage on AWS' high availability zones and security. However, this does come as an added cost. Apache Kafka is open-sourced and comes with a strong ecosystem of tools. Kafka is also known for high performance in throughput and low latency. However, using Kafka, it would make management more complex. Scaling would need to be done manually as well. 

Ultimately, I would prefer to use Kafka as I believe by having more control and customization over the data streaming, we would be able to eke out more performance benefits in the whole pipeline. 

## 2. Stream Processing 
In this phase, we would be reading the stock data and calculating the averages for the 20, 30 and 200 day moving averages. 

Possible options: 
- Spark Stream
- Kafka Stream 

Discussion: 

Spark Stream has fault tolerance via Resilient Distributed Datasets. Spark Stream also provides support for both batch and stream processing. However, Kafka Stream processes each record at a time whereas Spark Stream uses micro-batch processing. This enables Kafka to enjoy lower latency. 

Kafka Stream should be the choice if we are using Apache Kafka in the previous step. As our data pipeline prioritizes lower latency, we should use Kafka Stream over Spark Stream. 

## 3. Data Storage
After the averages have been calculated in the previous phase, they would be persisted in the database. 

Possible options:
- TimescaleDB
- InfluxDB 

Discussion: 
Both DBs are used to store time-series data. TimescaleDB is an extension of Postgres. This means there is extensive support with existing Postgres tools. InfluxDB is optimized for high speed and write. However, the downside of InfluxDB is that the language used is InfluxQL. Also, the support for InfluxDB's tools is not as extensive as TimescaleDB. 

I would choose TimescaleDB over InfluxDB so that I can leverage on the existing Postgres tools. An example would be `pg_state_statements`. This can be used to measure the performance oF SQL queries (in this case, the moving averages statements). 

## 4. API
An API can be built to access the data from the database. 

Possible options: 
- ExpressJS
- Flask (Python)

Discussion: 
The choice of API depends on the expertise of the team and their preference. Another consideration would be the existing languages and applications already built by the organization. If the majority of the applications are built in Python, it would be more appropriate to use Flask. Vice versa. 

