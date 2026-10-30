

import pandas as pd
import mysql.connector

from config import (
    MYSQL_CONFIG,
    RAW_DATABASE,
    RAW_TABLE,
    BATCH_SIZE
)


def load_raw_data(batch_number, df, reset=False):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{RAW_DATABASE}`"
        )

        cursor.execute(f"USE `{RAW_DATABASE}`")

        columns = [
            f"`{column}` LONGTEXT"
            for column in df.columns
        ]

        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS `{RAW_TABLE}` ("
            "raw_row_id BIGINT AUTO_INCREMENT PRIMARY KEY, "
            + ", ".join(columns)
            + ")"
        )

        if reset:
            cursor.execute(f"TRUNCATE TABLE `{RAW_TABLE}`")

        column_names = ", ".join(
            f"`{column}`" for column in df.columns
        )

        placeholders = ", ".join(
            ["%s"] * len(df.columns)
        )

        query = (
            f"INSERT INTO `{RAW_TABLE}` "
            f"({column_names}) VALUES ({placeholders})"
        )

        records = [
            tuple(
                None if pd.isna(value) or value == "" else str(value)
                for value in row
            )
            for row in df.itertuples(index=False, name=None)
        ]

        cursor.executemany(query, records)
        connection.commit()

        print(
            f"Raw Batch {batch_number}: "
            f"{cursor.rowcount} records loaded"
        )

        return len(records)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()