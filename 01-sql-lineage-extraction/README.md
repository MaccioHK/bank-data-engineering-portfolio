# Project 01 — SQL Lineage Extraction

## Goal
This project extracts basic SQL lineage from a query.

It identifies:
- source tables
- table aliases
- selected columns
- simple lineage mapping from source column to output column

## Example
Input SQL:

```sql
SELECT
    t.trade_id,
    t.amount,
    b.book_name
FROM trades t
JOIN books b
    ON t.book_id = b.book_id
WHERE t.trade_date >= DATE '2026-01-01';
