import pandas as pd
from config import CSV_FILE, BATCH_SIZE


def extract_data():
    batch_number = 1

    for batch in pd.read_csv(CSV_FILE, chunksize=BATCH_SIZE, dtype=str):
        print(
            f"Extracted Batch {batch_number}: "
            f"{len(batch)} records"
        )

        yield batch_number, batch

        batch_number += 1