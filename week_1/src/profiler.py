from pathlib import Path
import sqlite3
import math

def run_data_profile(db_path: Path):
	if (db_path.exists() == False):
		print(f"❌ Database not found at {db_path}")
		return
	
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("SELECT COUNT(source_id) FROM jobs;")
	total_records = cursor.fetchone()[0]


	cursor.execute("SELECT COUNT(source_id) FROM jobs WHERE job_title IS NULL;")
	null_job_title_records = cursor.fetchone()[0]

	cursor.execute("SELECT COUNT(source_id) FROM jobs WHERE company IS NULL;")
	null_company_records = cursor.fetchone()[0]

	cursor.execute("SELECT COUNT(source_id) FROM jobs WHERE description IS NULL;")
	null_description_records = cursor.fetchone()[0]

	cursor.execute("SELECT * FROM jobs ORDER BY LENGTH(description) DESC LIMIT 1;")
	longest_description_record = cursor.fetchone()

	cursor.execute("SELECT * FROM jobs ORDER BY LENGTH(description) ASC LIMIT 1;")
	shortest_description_record = cursor.fetchone()

	cursor.execute("SELECT AVG(LENGTH(description)) FROM jobs;")
	average_description_length = cursor.fetchone()[0]

	conn.close()
	print(
		"--- 🔍 DATA QUALITY REPORT ---\n"
		f"📈 Total Records: {total_records}\n"
		f"❓ Missing Values -> job_title: {null_job_title_records}, company: {null_company_records}, description: {null_description_records}\n"
		f"📝 Avg Description Length: {math.floor(average_description_length)} chars\n"
		f"⚠️  Shortest Description: {len(shortest_description_record[3])} chars\n"
   		f"\t↳ source_id: {shortest_description_record[0]} | job_title: {shortest_description_record[1]}\n"
		f"🚨 Longest Description: {len(longest_description_record[3])} chars\n"
		f"\t↳ source_id: {longest_description_record[0]} | job_title: {longest_description_record[1]}\n"
	)

	