import boto3
import csv
import os
import io
import re
from datetime import datetime

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket = os.environ["BUCKET_NAME"]
    cleaned_prefix = os.environ["CLEANED_PREFIX"]

    # Get the uploaded file info from event
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        print(f"Processing file: {key}")

        # Read raw file from S3
        raw_obj = s3.get_object(Bucket=bucket, Key=key)
        raw_data = raw_obj["Body"].read().decode("utf-8").splitlines()

        reader = csv.DictReader(raw_data)
        cleaned_rows = []

        seen_orders = set()

        for row in reader:
            # Deduplicate
            order_id = row["order_id"]
            if order_id in seen_orders:
                continue
            seen_orders.add(order_id)

            # Handle missing product
            if not row["product"]:
                row["product"] = "Unknown"

            # Fix date format
            try:
                if "-" in row["order_date"] and len(row["order_date"].split("-")[0]) == 2:
                    # Convert DD-MM-YYYY → YYYY-MM-DD
                    parsed_date = datetime.strptime(row["order_date"], "%d-%m-%Y")
                    row["order_date"] = parsed_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(f"Date parse error: {row['order_date']} - {e}")
                continue

            # Normalize region casing
            row["region"] = row["region"].title()

            # Compute line_total
            try:
                qty = int(row["quantity"])
                price = float(row["price"])
                row["line_total"] = round(qty * price, 2)
            except:
                row["line_total"] = 0.0

            cleaned_rows.append(row)

        # Save to CSV in memory
        output = io.StringIO()
        fieldnames = ["order_id", "product", "category", "quantity", "price", "order_date", "region", "line_total"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

        # Upload cleaned file to S3
        cleaned_key = key.replace("raw/", cleaned_prefix)
        s3.put_object(Bucket=bucket, Key=cleaned_key, Body=output.getvalue())

        print(f"✅ Cleaned file written to {cleaned_key}")

    return {
        'statusCode': 200,
        'body': f'Successfully processed {len(event["Records"])} files'
    }