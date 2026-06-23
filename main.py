import os
import re
import psycopg2
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

SITE_EMAIL = os.getenv("SITE_EMAIL")
SITE_PASSWORD = os.getenv("SITE_PASSWORD")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME"),
}


# --- Scraping ---

def scrape_problem(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.namastesql.com/login")
        page.wait_for_selector('input[name="email"]', timeout=15000)
        page.fill('input[name="email"]', SITE_EMAIL)
        page.fill('input[name="password"]', SITE_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_url(lambda u: "login" not in u, timeout=30000)

        page.goto(url)
        page.wait_for_selector('#runCodeBtn', timeout=30000)

        question_text = page.inner_text('#questionTxt')
        schema = ""
        if "Tables:" in question_text:
            schema = question_text[question_text.index("Tables:"):].strip()

        page.click('#runCodeBtn')
        page.wait_for_function(
            "document.querySelector('#output-view') && document.querySelector('#output-view').innerText.trim().length > 0",
            timeout=30000
        )
        table_data = page.inner_text('#output-view').strip()

        browser.close()
        return schema, table_data


# --- Parsing ---

def parse_ascii_table(block):
    headers, rows = [], []
    lines = [l for l in block.strip().splitlines() if l.strip().startswith("|")]
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if i == 0:
            headers = cells
        else:
            rows.append(cells)
    return headers, rows


def parse_schema(schema_text):
    tables = []
    parts = re.split(r'Tables:\s*(\w+)', schema_text)
    it = iter(parts[1:])
    for table_name, block in zip(it, it):
        headers, rows = parse_ascii_table(block)
        columns = [(r[0], r[1]) for r in rows if r[0].upper() != "COLUMN_NAME"]
        if columns:
            tables.append((table_name.strip(), columns))
    return tables


def parse_data(data_text):
    results = []
    lines = data_text.strip().splitlines()
    i = 0
    while i < len(lines):
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
    if val.lstrip("-").isdigit():
        return int(val)
    try:
        return float(val)
    except ValueError:
        return val if val.upper() != "NULL" else None


# --- Database ---

def load_to_db(tables_schema, tables_data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for (table_name, columns), (headers, rows) in zip(tables_schema, tables_data):
        print(f"\nProcessing table: {table_name}")
        col_defs = ", ".join(f'"{col}" {dtype}' for col, dtype in columns)
        cur.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
        cur.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
        print(f"  Created table with columns: {[c[0] for c in columns]}")

        placeholders = ", ".join(["%s"] * len(headers))
        col_names = ", ".join(f'"{h}"' for h in headers)
        insert_sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
        for row in rows:
            cur.execute(insert_sql, [infer_value(v) for v in row])
        print(f"  Inserted {len(rows)} rows")

    conn.commit()
    cur.close()
    conn.close()


# --- Entry point ---

def main():
    url = input("Enter problem URL: ").strip()

    print("\nScraping problem...")
    schema, table_data = scrape_problem(url)

    content = f"=== TABLE SCHEMA ===\n{schema}\n\n=== TABLE DATA ===\n{table_data}\n"
    with open("problem_data.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Saved to problem_data.txt")

    tables_schema = parse_schema(schema)
    tables_data = parse_data(table_data)

    if not tables_schema:
        print("No schema found — skipping DB load.")
        return

    pairs = list(zip(tables_schema, tables_data))
    load_to_db([s for s, _ in pairs], [d for _, d in pairs])
    print("\nDone.")


if __name__ == "__main__":
    main()
