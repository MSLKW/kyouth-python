from pathlib import Path
import sqlite3
from prompt_model import prompt_model
import re

def batch_update(conn: sqlite3.Connection, model: str, batch_amount: int):
	read_cursor = conn.cursor()
	write_cursor = conn.cursor()
	data_set_pattern = r"\(([^:]+):([^)]+)\)"
	read_cursor.execute('''
		SELECT source_id, description FROM jobs WHERE tech_stack IS NULL;
	''')
	batch_index = 0
	while True:
		null_tech_stacks = read_cursor.fetchmany(batch_amount)
		if not null_tech_stacks:
			break
		print(f"Batch[{batch_index}]")
		batch_index += 1
		prompt = f'''Gather the technology stack from the dataset provided and present it in a list formatted as (source_id:tech_stack) separated by ", ".
			An example would be "C, C++, Java, Python, Ollama, Gemini, API". 
			If the description does not have any relevant tech_stack in them, put N/A as the tech_stack.
			The dataset provided is formatted as (source_id:description), ...
			Do not say anything else other than the technology stack. The dataset provided: '''
		for item in null_tech_stacks:
			source_id = item[0]
			description = item[1]
			prompt += f"({source_id}:{description}), "

		try:
			result = prompt_model(
				model=model,
				prompt=prompt
			)
		except Exception as e:
			print(f"Encountered an error when prompting model {model}")
			print(e)
			return

		pairs = re.findall(data_set_pattern, result)
		write_cursor.executemany('''
			UPDATE jobs SET tech_stack = ? WHERE source_id = ?;
		''', [(tech_stack, source_id) for source_id, tech_stack in pairs])
		conn.commit()
		for source_id, tech_stack in pairs:
			print(f"Analyzed Job {source_id}: {tech_stack}")
	if batch_index == 0:
		print("Could not find NULL tech_stack in database")


def tag_data(db_url: str):
	db_path = Path(db_url)
	if (db_path.exists() == False):
		print(f"Error: Cannot find database at {db_path}")
		return
	conn = sqlite3.connect(db_path)
	batch_update(conn, "gemini-2.5-flash", 30)
	conn.close()


if __name__ == "__main__":
	tag_data("./data/jobs_d1.db")