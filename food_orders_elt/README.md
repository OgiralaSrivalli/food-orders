# Food Orders ELT Pipeline

## Project Description

This project implements an ELT pipeline using Python, Pandas,
and MySQL.

The pipeline extracts food order data from a CSV file,
loads the original data into a raw MySQL database,
transforms and validates the data, and loads the cleaned
data into an analytics database.

## Project Structure

- config.py: Project configuration
- extract.py: Extract CSV data in batches
- load_raw.py: Load original records into MySQL
- retrieve_raw.py: Retrieve raw records in batches
- transform.py: Clean and transform data
- validate.py: Validate transformed data
- load_transformed.py: Load cleaned records into MySQL
- elt_batch_pipeline.py: Run the complete pipeline
- business_analysis.sql: Business analysis queries
- requirements.txt: Required Python libraries
- output/: Generated output files

## Requirements

- Python
- MySQL Server
- Pandas
- MySQL Connector for Python

## Installation

Install the required libraries:

pip install -r requirements.txt

## Configuration

Update the MySQL username and password in config.py
or configure the MYSQL_PASSWORD environment variable.

Place food_orders.csv in the project folder.

## Run the Pipeline

python elt_batch_pipeline.py

## Output Files

The output folder contains:

- cleaned_food_orders.csv
- rejected_records.csv
- validation_report.json

## Databases

Raw database: food_orders_raw_db

Raw table: raw_food_orders

Analytics database: food_orders_analytics_db

Analytics table: cleaned_food_orders