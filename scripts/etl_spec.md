# ETL Transformation Rules

1. Remove duplicate `order_id`s.
2. Drop rows missing `order_date` or `product`.
3. Convert `order_date` to ISO format `YYYY-MM-DD`.
4. Calculate `line_total = quantity * price`.
5. Normalize `region` names to title case.