import pandas as pd
from io import BytesIO
from sqlalchemy import text
from datetime import datetime

from config import BUCKET_NAME, S3_FOLDER
from utils.s3_utils import connect_s3
from utils.postgres_utils import connect_postgres
from utils.validation import preprocess_dataframe


def main():

    print("Starting ETL Process...")

    # Connect to S3
    s3 = connect_s3()
    print("Connected to S3")

    # Connect to PostgreSQL
    engine = connect_postgres()
    print("Connected to PostgreSQL")

    # Get all files from S3 folder
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=S3_FOLDER
    )

    if 'Contents' not in response:
        print("No files found.")
        return

    # Process each file
    for obj in response['Contents']:

        file_key = obj['Key']

        # Skip non-parquet files
        if not file_key.endswith(".parquet"):
            continue

        # Check whether file already processed
        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM processed_files
                    WHERE file_name = :file_name
                """),
                {"file_name": file_key}
            )

            count = result.scalar()

        if count > 0:

            print(f"{file_key} already processed. Skipping.")
            continue

        print(f"\nProcessing file: {file_key}")

        try:

            # Download file from S3
            file_obj = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=file_key
            )

            # Read parquet file
            df = pd.read_parquet(
                BytesIO(file_obj["Body"].read()),
                engine="pyarrow"
            )

            print(f"Rows found: {len(df)}")

            # Data preprocessing
            df = preprocess_dataframe(df)

            # Insert data in chunks
            chunk_size = 1000

            for i in range(0, len(df), chunk_size):

                chunk = df.iloc[i:i + chunk_size]

                chunk.to_sql(
                    "VKABTEST",
                    engine,
                    if_exists="append",
                    index=False,
                    method="multi"
                )

                print(
                    f"Inserted rows {i} to {min(i + chunk_size, len(df))}"
                )

            # Mark file as processed
            with engine.connect() as conn:

                conn.execute(
                    text("""
                        INSERT INTO processed_files (file_name, processed_time)
                        VALUES (:file_name, :processed_time)
                    """),
                    {"file_name": file_key, 
                     "processed_time" : datetime.now()}
                )

                conn.commit()

            print(f"{file_key} loaded successfully.")

        except Exception as e:

            print(f"Error processing file: {file_key}")
            print(str(e))

    print("\nETL Process Completed Successfully.")


if __name__ == "__main__":
    main()