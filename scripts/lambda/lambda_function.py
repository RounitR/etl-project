"""
lambda_function.py
ETL Lambda: read CSV from s3://<bucket>/raw/<file>, clean rows, write CSV to s3://<bucket>/cleaned/<file>, move original to processed/
Saves CloudWatch logs. No Snowflake connector here (we'll use COPY INTO from Snowflake afterwards).
"""

import boto3
import csv
import io
import os
import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

# Environment variables (set in Lambda Configuration)
BUCKET = os.environ.get("S3_BUCKET", "etl-retail-data-rounit")
RAW_PREFIX = os.environ.get("S3_RAW_PREFIX", "raw/")
CLEANED_PREFIX = os.environ.get("S3_CLEANED_PREFIX", "cleaned/")
PROCESSED_PREFIX = os.environ.get("S3_PROCESSED_PREFIX", "processed/")

# Acceptable date formats to parse
DATE_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"]

def parse_date_to_iso(datestr: str):
    if not datestr:
        return None
    datestr = datestr.strip()
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(datestr, fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    # Attempt heuristic: if ISO-like already with time portion
    try:
        dt = datetime.fromisoformat(datestr)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def process_s3_object(bucket: str, key: str):
    logger.info(f"Start processing s3://{bucket}/{key}")
    # Read object
    resp = s3.get_object(Bucket=bucket, Key=key)
    raw_bytes = resp["Body"].read()
    raw_text = raw_bytes.decode("utf-8", errors="replace")
    lines = raw_text.splitlines()

    reader = csv.DictReader(lines)
    fieldnames_out = ["order_id", "product", "category", "quantity", "price", "order_date", "region", "line_total"]

    seen = set()
    cleaned_rows = []

    for row in reader:
        # Basic trimming
        order_id = (row.get("order_id") or "").strip()
        product = (row.get("product") or "").strip()
        category = (row.get("category") or "").strip()
        quantity_raw = (row.get("quantity") or "").strip()
        price_raw = (row.get("price") or "").strip()
        order_date_raw = (row.get("order_date") or "").strip()
        region_raw = (row.get("region") or "").strip()

        # Skip if order_id missing
        if order_id == "":
            logger.info("Skipping row with empty order_id")
            continue

        # Deduplicate
        if order_id in seen:
            # keep first occurrence only
            continue
        seen.add(order_id)

        # Drop rows with missing product (per spec)
        if product == "":
            logger.info(f"Skipping order_id {order_id} because product missing")
            continue

        # Parse quantity and price
        try:
            quantity = int(quantity_raw)
        except Exception:
            logger.info(f"Skipping order_id {order_id} due to invalid quantity: {quantity_raw}")
            continue

        try:
            price = float(price_raw)
        except Exception:
            # If incoming 'price' looks like total (generator used total), it's still a float - we'll try to handle below
            logger.info(f"Skipping order_id {order_id} due to invalid price: {price_raw}")
            continue

        # Standardize date
        iso_date = parse_date_to_iso(order_date_raw)
        if not iso_date:
            logger.info(f"Skipping order_id {order_id} due to invalid date format: {order_date_raw}")
            continue

        # Normalize region to title case
        region = region_raw.title() if region_raw else "Unknown"

        # Compute line_total:
        # We assume incoming 'price' is unit price. If your generator produced total price instead, you can either:
        # - regenerate data with per-unit price, or
        # - use fallback: treat 'price' as total if price >= quantity * 1 (logical heuristic)
        # Here we compute line_total = quantity * price (standard).
        line_total = round(quantity * price, 2)

        cleaned_rows.append({
            "order_id": order_id,
            "product": product,
            "category": category,
            "quantity": quantity,
            "price": price,
            "order_date": iso_date,
            "region": region,
            "line_total": line_total
        })

    if not cleaned_rows:
        logger.info("No cleaned rows to write. Finishing without writing a file.")
        # still move original to processed to avoid reprocessing
        move_raw_to_processed(bucket, key)
        return

    # Write cleaned CSV to memory
    out_buf = io.StringIO()
    writer = csv.DictWriter(out_buf, fieldnames=fieldnames_out)
    writer.writeheader()
    writer.writerows(cleaned_rows)
    out_body = out_buf.getvalue().encode("utf-8")

    # Produce cleaned key
    filename = key.split("/")[-1]
    cleaned_key = f"{CLEANED_PREFIX}{filename}"
    # Upload cleaned file
    s3.put_object(Bucket=bucket, Key=cleaned_key, Body=out_body)
    logger.info(f"Cleaned file written to s3://{bucket}/{cleaned_key}")

    # Move raw to processed (copy then delete)
    move_raw_to_processed(bucket, key)

def move_raw_to_processed(bucket, key):
    filename = key.split("/")[-1]
    dest_key = f"{PROCESSED_PREFIX}{filename}"
    # copy
    copy_source = {"Bucket": bucket, "Key": key}
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=dest_key)
    # delete original
    s3.delete_object(Bucket=bucket, Key=key)
    logger.info(f"Moved original file to s3://{bucket}/{dest_key}")

def lambda_handler(event, context):
    logger.info("Lambda triggered")
    try:
        for record in event.get("Records", []):
            s3_info = record.get("s3", {})
            bucket = s3_info.get("bucket", {}).get("name")
            key = s3_info.get("object", {}).get("key")
            if not bucket or not key:
                continue
            process_s3_object(bucket, key)
    except Exception as e:
        logger.exception("Error in lambda_handler")
        raise
    return {"status": "ok"}

# Local testing helper (run in VS Code)
def process_local_file(path):
    # Simulate local file processing by reading and processing CSV then writing to local cleaned file
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    reader = csv.DictReader(lines)
    temp_key = "local_test.csv"
    # Create a tiny in-memory "s3" by writing to local cleaned file
    cleaned_rows = []
    seen = set()
    for row in reader:
        order_id = (row.get("order_id") or "").strip()
        product = (row.get("product") or "").strip()
        if order_id == "" or product == "":
            continue
        if order_id in seen:
            continue
        seen.add(order_id)
        try:
            quantity = int((row.get("quantity") or "0").strip())
            price = float((row.get("price") or "0").strip())
        except:
            continue
        iso_date = parse_date_to_iso((row.get("order_date") or "").strip())
        if not iso_date:
            continue
        region = (row.get("region") or "").strip().title()
        cleaned_rows.append({
            "order_id": order_id,
            "product": product,
            "category": (row.get("category") or "").strip(),
            "quantity": quantity,
            "price": price,
            "order_date": iso_date,
            "region": region,
            "line_total": round(quantity * price, 2)
        })
    out_path = path.replace(".csv", "_cleaned.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["order_id","product","category","quantity","price","order_date","region","line_total"])
        writer.writeheader()
        writer.writerows(cleaned_rows)
    print(f"Local cleaned file written to {out_path}")

if __name__ == "__main__":
    # Local quick test
    sample = "../data/sample_sales_dirty.csv"
    print("Running local test on", sample)
    process_local_file(sample)
