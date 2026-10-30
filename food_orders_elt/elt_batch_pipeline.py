import os
import json
import pandas as pd

from config import OUTPUT_DIR
from extract import extract_data
from load_raw import load_raw_data
from retrieve_raw import retrieve_raw_data
from transform import transform_data
from validate import validate_data
from load_transformed import load_transformed_data


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_extracted = 0
    total_raw_loaded = 0
    total_retrieved = 0
    batches_processed = 0

    print("\nSTEP 1: EXTRACT AND LOAD RAW DATA")

    # Extract CSV batches and load original data into MySQL
    for batch_number, batch in extract_data():
        batches_processed += 1
        total_extracted += len(batch)

        loaded = load_raw_data(
            batch_number,
            batch,
            reset=(batch_number == 1)
        )

        total_raw_loaded += loaded

    print("\nSTEP 2: RETRIEVE AND TRANSFORM DATA")

    cleaned_batches = []
    rejected_batches = []

    for batch_number, batch in retrieve_raw_data():
        total_retrieved += len(batch)

        cleaned, rejected = transform_data(batch)

        cleaned_batches.append(cleaned)

        if not rejected.empty:
            rejected_batches.append(rejected)

        print(
            f"Transformed batch {batch_number}: "
            f"{len(cleaned)} valid records, "
            f"{len(rejected)} rejected records"
        )

    # Combine all transformed batches
    cleaned_df = (
        pd.concat(cleaned_batches, ignore_index=True)
        if cleaned_batches
        else pd.DataFrame()
    )

    rejected_df = (
        pd.concat(rejected_batches, ignore_index=True)
        if rejected_batches
        else pd.DataFrame()
    )

    # Save output files
    cleaned_path = os.path.join(
        OUTPUT_DIR, "cleaned_food_orders.csv"
    )

    rejected_path = os.path.join(
        OUTPUT_DIR, "rejected_records.csv"
    )

    cleaned_df.to_csv(cleaned_path, index=False)
    rejected_df.to_csv(rejected_path, index=False)

    print("\nSTEP 3: VALIDATE DATA")

    validation_report = validate_data(
        cleaned_df,
        rejected_df
    )

    print("\nSTEP 4: LOAD ANALYTICS DATABASE")

    total_analytics_loaded = load_transformed_data(
        cleaned_df
    )

    # Final execution report
    report = {
        "total_extracted": total_extracted,
        "batches_processed": batches_processed,
        "raw_records_loaded": total_raw_loaded,
        "raw_records_retrieved": total_retrieved,
        "valid_records_transformed": len(cleaned_df),
        "rejected_records": len(rejected_df),
        "analytics_records_loaded": total_analytics_loaded,
        "validation_status": validation_report[
            "validation_status"
        ],
        "validation_details": validation_report
    }

    report_path = os.path.join(
        OUTPUT_DIR, "validation_report.json"
    )

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    print("\nELT PIPELINE COMPLETED")
    print("----------------------")
    print(json.dumps(report, indent=4, default=str))


if __name__ == "__main__":
    main()