import re
import json
from pathlib import Path


def extract_tables(sql_text: str):
    """
    Extract table names and aliases from FROM / JOIN clauses.
    Example:
        FROM trades t
        JOIN books b
    Returns:
        {'t': 'trades', 'b': 'books'}
    """
    pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z_][\w]*)\s+([a-zA-Z_][\w]*)'
    matches = re.findall(pattern, sql_text, re.IGNORECASE)
    return {alias: table for table, alias in matches}


def extract_select_columns(sql_text: str):
    """
    Extract columns from SELECT section.
    Example:
        t.trade_id,
        t.amount,
        b.book_name
    Returns:
        [('t', 'trade_id'), ('t', 'amount'), ('b', 'book_name')]
    """
    select_match = re.search(r'SELECT(.*?)FROM', sql_text, re.IGNORECASE | re.DOTALL)
    if not select_match:
        return []

    select_part = select_match.group(1)
    columns = []

    for line in select_part.split(','):
        line = line.strip()
        match = re.match(r'([a-zA-Z_][\w]*)\.([a-zA-Z_][\w]*)', line)
        if match:
            alias, column = match.groups()
            columns.append((alias, column))

    return columns


def build_lineage(sql_text: str):
    tables = extract_tables(sql_text)
    columns = extract_select_columns(sql_text)

    lineage = []
    for alias, column in columns:
        source_table = tables.get(alias, "UNKNOWN")
        lineage.append({
            "source_table": source_table,
            "source_column": column,
            "output_column": column
        })

    return {
        "tables": tables,
        "lineage": lineage
    }


def main():
    input_file = Path("data/sample.sql")
    output_file = Path("output/lineage.json")

    sql_text = input_file.read_text()
    result = build_lineage(sql_text)

    output_file.write_text(json.dumps(result, indent=4))
    print("Lineage written to", output_file)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
