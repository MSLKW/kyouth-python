from pathlib import Path
import sqlite3
import json


def load_json_into_db(cursor: sqlite3.Cursor, json_file: Path):
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
        cursor.execute(
            """
			INSERT OR IGNORE INTO jobs (
				source_id, job_title, company, description	
			) VALUES (?, ?, ?, ?);
		""",
            (
                json_data["source_id"],
                json_data["job_title"],
                json_data["company"],
                json_data["description"],
            ),
        )
        inserted_row = cursor.rowcount
        if inserted_row == 0:
            return (False, f"Skipped (duplicate): {json_file.name}")
    return (True, "Success")


#
# Assumes that output_dir has the GOLD_DIR + DB_NAME
#
def load_all_jsons(input_dir: Path, output_db: Path):
    if not input_dir.exists():
        print(f"Error: {input_dir} does not exist")
        return
    if not output_db.parent.exists():
        print(f"⚠️  Warning: {output_db.parent} does not exist, creating the directory")
        output_db.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(output_db)
    cursor = conn.cursor()
    cursor.execute(""" 
		CREATE TABLE IF NOT EXISTS jobs (
			source_id TEXT PRIMARY KEY,
			job_title TEXT NOT NULL,
			company TEXT NOT NULL,
			description TEXT NOT NULL,
			tech_stack TEXT NULL
		);
	""")

    inserted_total = 0
    skipped_total = 0

    for item in input_dir.glob("*.json"):
        status, msg = load_json_into_db(cursor, item)
        if status:
            print(f"✅ Inserted: {item.name}")
            inserted_total += 1
        elif not status:
            print(f"⏭️  {msg}")
            skipped_total += 1
    conn.commit()
    conn.close()
    print(
        f"\n📊 Gold Summary:\nTotal: {inserted_total + skipped_total} | Inserted: {inserted_total} | Skipped: {skipped_total}"
    )
