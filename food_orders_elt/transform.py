import pandas as pd

seen_rows = set()


def transform_data(df):
    global seen_rows

    df = df.copy()
    rejected = []

    # Remove duplicate records, including duplicates across batches
    row_keys = df.astype(object).where(
        pd.notna(df), None
    ).apply(lambda row: tuple(row), axis=1)

    duplicate_mask = row_keys.apply(
        lambda key: key in seen_rows
    )

    for key in row_keys:
        seen_rows.add(key)

    if duplicate_mask.any():
        duplicate_rows = df.loc[duplicate_mask].copy()
        duplicate_rows["Rejection Reason"] = "Duplicate record"
        rejected.append(duplicate_rows)

    df = df.loc[~duplicate_mask].copy()

    # Convert timestamp columns
    date_columns = [
        "Order Date and Time",
        "Delivery Date and Time"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column], errors="coerce"
        )

    # Convert financial columns to numeric values
    financial_columns = [
        "Order Value",
        "Delivery Fee",
        "Commission Fee",
        "Payment Processing Fee",
        "Refunds/Chargebacks"
    ]

    for column in financial_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # Calculate delivery time
    df["Delivery_Time_Minutes"] = (
        df["Delivery Date and Time"] -
        df["Order Date and Time"]
    ).dt.total_seconds() / 60

    # Identify invalid timestamps and negative delivery times
    invalid_timestamp = (
        df["Order Date and Time"].isna() |
        df["Delivery Date and Time"].isna()
    )

    negative_delivery = df["Delivery_Time_Minutes"] < 0

    invalid_mask = invalid_timestamp | negative_delivery

    if invalid_mask.any():
        invalid_rows = df.loc[invalid_mask].copy()

        invalid_rows["Rejection Reason"] = invalid_rows.apply(
            lambda row: (
                "Invalid or missing timestamp"
                if pd.isna(row["Order Date and Time"])
                or pd.isna(row["Delivery Date and Time"])
                else "Negative delivery time"
            ),
            axis=1
        )

        rejected.append(invalid_rows)

    df = df.loc[~invalid_mask].copy()

    # Add order date and order hour
    df["Order_Date"] = df["Order Date and Time"].dt.date
    df["Order_Hour"] = df["Order Date and Time"].dt.hour

    # Calculate platform net revenue
    revenue_columns = [
        "Commission Fee",
        "Payment Processing Fee",
        "Refunds/Chargebacks"
    ]

    df["Platform_Net_Revenue"] = pd.NA

    revenue_mask = df[revenue_columns].notna().all(axis=1)

    df.loc[revenue_mask, "Platform_Net_Revenue"] = (
        df.loc[revenue_mask, "Commission Fee"]
        + df.loc[revenue_mask, "Payment Processing Fee"]
        - df.loc[revenue_mask, "Refunds/Chargebacks"]
    )

    # Handle missing categorical values
    if "Payment Method" in df.columns:
        df["Payment Method"] = (
            df["Payment Method"].fillna("Unknown")
        )

    if "Discounts and Offers" in df.columns:
        df["Discounts and Offers"] = (
            df["Discounts and Offers"]
            .fillna("Not Specified")
        )

    rejected_df = (
        pd.concat(rejected, ignore_index=True)
        if rejected
        else pd.DataFrame()
    )

    return df, rejected_df