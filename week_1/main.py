import sys
from pathlib import Path
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
# from src.loader import load_all_jsons
# from src.run_data_profile import run_data_profile

SOURCE_DIR = Path("data/0_source")
BRONZE_DIR = Path("data/1_bronze")
SILVER_DIR = Path("data/2_silver")
GOLD_DIR = Path("data/3_gold")
DB_NAME = "jobs.db"

# def run_profiler():
# 	db_path = GOLD_DIR/DB_NAME
# 	run_data_profile(db_path)

# def run_gold():
# 	input_dir = SILVER_DIR
# 	output_dir = GOLD_DIR
# 	load_all_jsons(input_dir, output_dir)

# def run_silver():
# 	input_dir = BRONZE_DIR
# 	output_dir = SILVER_DIR
# 	process_all_html(input_dir, output_dir)

def run_bronze():
	input_dir = SOURCE_DIR
	output_dir = BRONZE_DIR
	ingest_all_mhtml(input_dir, output_dir)
    
def main():
	total_args = len(sys.argv)
	if (total_args != 2):
		print("Error: wrong number of arguments", file=sys.stderr)
		sys.exit(1)
	argument = sys.argv[1]
	# use match/case
	match (argument):
		case "ingest":
			print("🥉 Bronze: Running \"ingest\" command")
			ingest_all_mhtml(SOURCE_DIR, BRONZE_DIR)
		case "process":
			print("🥈 Silver: Running \"process\" command")
			process_all_html(BRONZE_DIR, SILVER_DIR)
		case _:
			print(f"Error: Unknown command: {argument}")
	sys.exit(0)

	

if __name__ == "__main__":
	main()