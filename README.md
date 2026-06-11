# Project Description

The goal of the project is to learn more about Python and Data Engineering.

# Preamble

README.md is on the assumption that the project is on Windows OS, running it on Linux or macOS may require different commands than the ones provided to achieve the same effect

# Setup Instructions

Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

## Prerequisites

Required python version is 3.14

Run `uv python install`, `uv init`, `uv venv` to create python virtual environment

Dependencies required:
  - bs4 (0.0.2)
  - pydantic (2.13.4)
  - ruff (0.15.16)

Use `uv add bs4 ruff pydantic` to add the required dependencies

# Usage

Usage of the project will be described in each week's README.md

To run python scripts, use `uv run <script>.py`

To get into the venv and run python directly, run `.venv\Scripts\activate.ps1` on powershell to run `python main.py`

# Technical Reflections

Technical reflections of the project will be described in each week's README.md