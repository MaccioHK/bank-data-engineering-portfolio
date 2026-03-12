SELECT
    t.trade_id,
    t.amount,
    b.book_name
FROM trades t
JOIN books b
    ON t.book_id = b.book_id
WHERE t.trade_date >= DATE '2026-01-01';

