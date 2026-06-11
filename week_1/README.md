# WEEK 1

## Usage

Change directory into the week_1 folder: `cd week_1`
Run `uv run main.py` with any of the following commands `ingest`, `process`, `load`, `profile`, `all`

`ingest` will take mhtml files from data/0_source and output html files to data/1_bronze

`process` will take html files from data/1_bronze and output json files to data/2_silver

`load` will take json files from data/2_silver and output a jobs.db to data/3_gold

`profile` will take jobs.db and output a profile summary in the terminal

`all` will run the four commands above in sequence

## Technical Reflections

### Day 1: The Extractor (Medallion & Lakehouses)
Why is it useful to keep the original raw HTML files instead of directly inserting processed data into the database? What problems become easier to debug or recover from?
- **Answer**: It's useful to keep original raw HTML files because if there are any problems during the processing to silver or gold, we do not need to reingest data directly from the source. Also making it easier to process the data as the silver processor does not need to go into the mhtml source files, instead just opting to deal with the ingested html files from the bronze layer.

### Day 2: Treatment Plant (ETL vs ELT & Scale)
Why do cloud systems prefer loading raw data first before cleaning it (ELT)? What problems happen when processing files sequentially, and how does distributed processing help?
- **Answer**: Cloud systems prefer ELT instead of ETL because ELT extracts and loads the data immediately before having to transform it, allowing the data to be available quicker. Sequential processing of files can be slow for massive datasets as it's going to have to do processing for each file, but it is possible to help speed it up by using distributed processing as it's concurrent.

### Day 3: The Blueprint & The Vault (Storage & Contracts)
What should happen if an important field like job_title disappears? Why fail early instead of silently inserting nulls into DB? How does INSERT OR IGNORE help prevent duplicate records?
- **Answer**: Failing early instead of inserting nulls into the database helps to ensure that the database does not have any NULL elements in it when doing any read operations, it helps maintain integrity of the records in the database. INSERT OR IGNORE helps prevent duplicates by not inserting a record that has constraint violations.

### Day 4: The QA Inspector & Orchestrator (Orchestration & DAGs)
What happens if processor.py crashes halfway? How are automated orchestration tools more reliable than manual retries with Python scripts?
- **Answer**: If processor.py crashes halfway, which shouldn't be possible as any error in data would simply be skipped and moving on to the next, unless the input data is completely non-existent, in which then the ingestor.py would be at fault, or the source files itself is missing. Automated orchestration tools are more reliable as they run the whole pipeline, meaning that a human won't simply run processor.py without running ingestor.py, causing the ingestor.py to crash as there wouldn't be any input files for it.