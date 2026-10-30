import pandas as pd


def validate_data(df, rejected_df):
    report = {
        "valid_records": int(len(df)),
        "rejected_records": int(len(rejected_df)),
        "missing_values": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "duplicate_records": int(
            df.duplicated().sum()
        ),
        "negative_delivery_times": int(
            (df["Delivery_Time_Minutes"] < 0).sum()
        ) if "Delivery_Time_Minutes" in df.columns else 0,
        "validation_status": "PASS"
    }

    if (
        report["duplicate_records"] > 0
        or report["negative_delivery_times"] > 0
    ):
        report["validation_status"] = "FAIL"

    print("\nVALIDATION REPORT")
    print("-----------------")
    print("Valid records:", report["valid_records"])
    print("Rejected records:", report["rejected_records"])
    print("Duplicates:", report["duplicate_records"])
    print(
        "Validation status:",
        report["validation_status"]
    )

    return report