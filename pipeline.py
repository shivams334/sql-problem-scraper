import re
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "admin",
    "password": "admin123",
    "dbname": "practice_db",
}


def parse_ascii_table(block):
    """Parse an ASCII +---+---+ style table, return (headers, rows)."""
    rows = []
    headers = []
    lines = [l for l in block.strip().splitlines() if l.strip().startswith("|")]
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if i == 0:
            headers = cells
        else:
            rows.append(cells)
    return headers, rows


def parse_schema(schema_text):
    """Return list of (table_name, [(col_name, data_type), ...])."""
    tables = []
    # Split on "Tables: X" markers
    parts = re.split(r'Tables:\s*(\w+)', schema_text)
    # parts = [pre, name1, block1, name2, block2, ...]
    it = iter(parts[1:])
    for table_name, block in zip(it, it):
        headers, rows = parse_ascii_table(block)
        # Skip the header row (COLUMN_NAME / DATA_TYPE) — it's always index 0
        columns = [(r[0], r[1]) for r in rows if r[0].upper() != "COLUMN_NAME"]
        if columns:
            tables.append((table_name.strip(), columns))
    return tables


def parse_data(data_text):
    """Return list of (headers, rows) for each result table found."""
    results = []
    lines = data_text.strip().splitlines()
    i = 0
    while i < len(lines):
        # A table block starts with a separator line
        if re.match(r'^\+[-+]+\+$', lines[i].strip()):
            block = []
            while i < len(lines) and (lines[i].strip().startswith("+") or lines[i].strip().startswith("|")):
                block.append(lines[i])
                i += 1
            headers, rows = parse_ascii_table("\n".join(block))
            if headers:
                results.append((headers, rows))
        else:
            i += 1
    return results


def infer_value(val):
    """Return a Python-typed value for insertion."""
    if val.lstrip("-").isdigit():
        return int(val)
    try:
        return float(val)
    except ValueError:
        return val if val.upper() != "NULL" else None


def create_and_populate(tables_schema, tables_data):
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    for (table_name, columns), (headers, rows) in zip(tables_schema, tables_data):
        print(f"\nProcessing table: {table_name}")

        # Build CREATE TABLE
        col_defs = ", ".join(f'"{col}" {dtype}' for col, dtype in columns)
        cur.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
        cur.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
        print(f"  Created table with columns: {[c[0] for c in columns]}")

        # Insert rows
        placeholders = ", ".join(["%s"] * len(headers))
        col_names = ", ".join(f'"{h}"' for h in headers)
        insert_sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
        for row in rows:
            values = [infer_value(v) for v in row]
            cur.execute(insert_sql, values)
        print(f"  Inserted {len(rows)} rows")

    conn.commit()
    cur.close()
    conn.close()
    print("\nDone.")


def main():
    with open("problem_data.txt", encoding="utf-8") as f:
        content = f.read()

    schema_text = content.split("=== TABLE SCHEMA ===")[1].split("=== TABLE DATA ===")[0]
    data_text = content.split("=== TABLE DATA ===")[1]

    tables_schema = parse_schema(schema_text)
    tables_data = parse_data(data_text)

    if not tables_schema:
        print("No schema found in problem_data.txt")
        return
    if len(tables_schema) != len(tables_data):
        print(f"Warning: found {len(tables_schema)} schema(s) but {len(tables_data)} data table(s) — pairing what we can")

    pairs = list(zip(tables_schema, tables_data))
    create_and_populate([s for s, _ in pairs], [d for _, d in pairs])


if __name__ == "__main__":
    main()
