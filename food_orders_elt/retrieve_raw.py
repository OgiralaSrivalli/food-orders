import pandas as pd
import mysql.connector

from config import (
    MYSQL_CONFIG,
    RAW_DATABASE,
    RAW_TABLE,
    BATCH_SIZE
)


def retrieve_raw_data():
    connection = mysql.connector.connect(
        **MYSQL_CONFIG,
        database=RAW_DATABASE
    )

    try:
        query = f"SELECT * FROM `{RAW_TABLE}` ORDER BY raw_row_id"

        for batch_number, df in enumerate(
            pd.read_sql(query, connection, chunksize=BATCH_SIZE),
            start=1
        ):
            df = df.drop(columns=["raw_row_id"])

            print(
                f"Retrieved Batch {batch_number}: "
                f"{len(df)} records"
            )

            yield batch_number, df

    finally:
        connection.close()