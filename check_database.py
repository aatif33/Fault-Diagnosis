
import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "vortiq.db"

if not db_path.exists():
    print("ERROR: vortiq.db was not found.")
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("\n=== DATABASE TABLES ===")
for (table_name,) in tables:
    print(f"\nTable: {table_name}")

    cursor.execute(f'PRAGMA table_info("{table_name}")')
    columns = cursor.fetchall()

    for column in columns:
        print(" -", column[1])

    if table_name == "alarm_knowledge":
        cursor.execute(
            'SELECT * FROM "alarm_knowledge" '
            'WHERE UPPER(TRIM(alarm_code)) = ? LIMIT 1',
            ("SV0411",)
        )

        row = cursor.fetchone()

        if row:
            print("\n=== SV0411 SAMPLE RECORD ===")
            for column, value in zip(
                [item[1] for item in columns], row
            ):
                print(f"{column}: {value}")
        else:
            print("\nSV0411 was not found in this table.")

conn.close()
print("\nInspection complete. No data was modified.")
