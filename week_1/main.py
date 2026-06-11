import sys
from pathlib import Path
from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
from src.loader import load_all_jsons
from src.profiler import run_data_profile

SOURCE_DIR = Path("data/0_source")
BRONZE_DIR = Path("data/1_bronze")
SILVER_DIR = Path("data/2_silver")
GOLD_DIR = Path("data/3_gold")
DB_NAME = "jobs.db"


def main():
    total_args = len(sys.argv)
    if total_args != 2:
        print("Usage: python main.py [ingest|process|load|profile|all]")
        sys.exit(1)
    argument = sys.argv[1]
    match argument:
        case "ingest":
            print('🥉 Bronze: Running "ingest" command')
            ingest_all_mhtml(SOURCE_DIR, BRONZE_DIR)
        case "process":
            print('🥈 Silver: Running "process" command')
            process_all_html(BRONZE_DIR, SILVER_DIR)
        case "load":
            print('🥇 Gold: Running "load" command')
            load_all_jsons(SILVER_DIR, GOLD_DIR / DB_NAME)
        case "profile":
            print('🔍 Profile: Running "profile" command')
            run_data_profile(GOLD_DIR / DB_NAME)
        case "all":
            print('🌏 All: Running "all" command')
            ingest_all_mhtml(SOURCE_DIR, BRONZE_DIR)
            print("-----")
            process_all_html(BRONZE_DIR, SILVER_DIR)
            print("-----")
            load_all_jsons(SILVER_DIR, GOLD_DIR / DB_NAME)
            print("-----")
            run_data_profile(GOLD_DIR / DB_NAME)
        case _:
            print("Usage: python main.py [ingest|process|load|profile|all]")
    sys.exit(0)


if __name__ == "__main__":
    main()
