import os

CSV_FILE = "food_orders.csv"
BATCH_SIZE = 100
OUTPUT_DIR = "output"

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD", "Srivalli@2006")
}

RAW_DATABASE = "food_orders_raw_db"
RAW_TABLE = "raw_food_orders"

ANALYTICS_DATABASE = "food_orders_analytics_db"
ANALYTICS_TABLE = "cleaned_food_orders"