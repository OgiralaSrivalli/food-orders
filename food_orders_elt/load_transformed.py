import pandas as pd
import mysql.connector

from config import (
    MYSQL_CONFIG,
    ANALYTICS_DATABASE,
    ANALYTICS_TABLE,
    BATCH_SIZE
)


def load_transformed_data(df):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS "
            f"`{ANALYTICS_DATABASE}`"
        )
        cursor.execute(f"USE `{ANALYTICS_DATABASE}`")

        # Create columns using suitable MySQL data types
        column_definitions = []

        for column in df.columns:
            if column in [
                "Order Date and Time",
                "Delivery Date and Time"
            ]:
                sql_type = "DATETIME"
            elif column == "Order_Date":
                sql_type = "DATE"
            elif column in [
                "Order Value",
                "Delivery Fee",
                "Commission Fee",
                "Payment Processing Fee",
                "Refunds/Chargebacks",
                "Delivery_Time_Minutes",
                "Platform_Net_Revenue"
            ]:
                sql_type = "DOUBLE"
            elif column == "Order_Hour":
                sql_type = "INT"
            else:
                sql_type = "LONGTEXT"

            column_definitions.append(
                f"`{column}` {sql_type}"
            )

        cursor.execute(
            f"DROP TABLE IF EXISTS `{ANALYTICS_TABLE}`"
        )

        cursor.execute(
            f"CREATE TABLE `{ANALYTICS_TABLE}` ("
            + ", ".join(column_definitions)
            + ")"
        )

        if df.empty:
            connection.commit()
            print("No valid records to load.")
            return 0

        columns = ", ".join(
            f"`{column}`" for column in df.columns
        )

        placeholders = ", ".join(
            ["%s"] * len(df.columns)
        )

        query = (
            f"INSERT INTO `{ANALYTICS_TABLE}` "
            f"({columns}) VALUES ({placeholders})"
        )

        total_loaded = 0

        # Insert data in batches
        for start in range(0, len(df), BATCH_SIZE):
            batch = df.iloc[start:start + BATCH_SIZE]

            records = []

            for row in batch.itertuples(
                index=False, name=None
            ):
                values = []

                for value in row:
                    if pd.isna(value):
                        values.append(None)
                    elif isinstance(value, pd.Timestamp):
                        values.append(value.to_pydatetime())
                    else:
                        values.append(value)

                records.append(tuple(values))

            try:
                cursor.executemany(query, records)
                connection.commit()

                total_loaded += len(records)

                print(
                    f"Analytics batch loaded: "
                    f"{len(records)} records"
                )

            except Exception:
                connection.rollback()
                raise

        print("Total analytics records loaded:", total_loaded)

        return total_loaded

    finally:
        cursor.close()
        connection.close()