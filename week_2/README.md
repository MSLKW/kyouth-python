# Project Overview

The project has three modules: prompt_model.py, tag_data.py and find_skill_gaps.py

The project's goal is to utilize various LLMs and AI to tag data in an SQLite database with description input. It then uses the data tag to find missing skill gaps in a resume.

## Setup Instructions

Python version is 3.14

Python dependencies are:
  - google-genai (2.8.0)
  - ollama (0.6.2)
  - pydantic (2.13.4)
  - python-dotenv (1.2.2)

run `uv sync` to install dependencies listed in pyproject.toml. Or run `uv add` to add the dependencies manually

Create an API_KEY with google at [Google AI Studio](https://aistudio.google.com)

Create a `.env` file in the project, then write in `API_KEY=<fill_api_key_in_here>` in the file. Make sure that the .gitignore ignores the file before commiting

## Usage and API / Function Reference

`uv run prompt_model.py <model> <prompt>`

Input a model that the ollama servers support or the supported gemini models:
  - gemini-2.5-flash
  - gemini-2.5-flash-lite
  - gemini-3-flash-preview

prompt_model.py will be able to automatically select between the gemini models or the ollama models as long as the model input is correct.

Input a prompt for the model to process.

prompt_model.py will output a response from the LLM model.

`uv run tag_data.py`

tag_data.py will update the tech_stack column in the given db_url with relevant technologies sourced from the description column

tag_data.py will use prompt_model.py as a simple LLM API.

`uv run find_skill_gaps.py`

find_skill_gaps.py will collect all the tech_stacks in db_url and compares it with given technical skills in the resume provided. It will then output a pydantic model and outputs the missing skill gaps

find_skill_gaps.py will most likely use the data provided by tag_data.py in the database column tech_stack

## Data / Assumptions

The resume file should have a "Technical Skills:" keyword inside so that the find_skill_gaps module is able to find the technologies in the resume.

The project database should be supported by SQLite3.

The assumed Database Schema is as follows

source_id (TEXT, PRIMARY KEY) | job_title (TEXT, NOT NULL) | company (TEXT, NOT NULL) | description (TEXT, NOT NULL) | tech_stack (TEXT, NULLABLE)
--- | --- | --- | --- | ---
source_id | job_title | company | description | tech_stack

### Data Flow

The database should be sourced from week_1, with tech_stack column being NULL, then run tag_data.py to provide data to the tech_stack column, then run find_skill_gaps to output the missing skill gaps in the resume based on the database's tech_stack

## Testing

The project has been tested with the provided jobs_d1.db and resume_d3.txt

Determinism is ensured for find_skill_gaps.py as it's an algorithmic find function that requires a keyword to extract relevant tech stacks

## Limitations

find_skill_gaps module does not handle messy resumes with listed tech skills everywhere or without the "Technical Skills:" keyword. 

phi3 ollama model provides bad output such as unnecessary comments.

LLMs may take some time, so the scripts may take a few minutes to process.

# Architecture Reflection

### Desgin Choices
Why you structured your system the way you did (modularity, separation of concerns, etc.)
  - I separated prompt_model, tag_data and find_skill_gaps because their objectives are vastly different, so keeping it modular allows separation of responsibility

### Trade-offs
What you chose to prioritize (e.g. simplicity vs scalability, speed vs accuracy)
  - For parsing the resume, I chose to use a simple finding algorithm to extract the technical skills from the resume, this allowed me to have greater determinism since I didn't have to use an LLM. But definitely created a constraint where bad resume inputs will raise errors. However, I prioritized the determinism of the project over the potential bad input scenarios.

### Improvements
What you would change or extend if given more time (e.g. better architecture, optimizations, additional features)
  - I would try to optimize the token usage


# Explanations

Large Language Models are a great tool for analyzing messy data and extracting relevant information from data, however they can be a pain to work with as they provide undeterministic outputs.