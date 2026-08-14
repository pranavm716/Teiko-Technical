.PHONY: setup

setup:
	pip install uv
	uv sync

pipeline:
	.venv/bin/python load_data.py
	.venv/bin/python run_analysis.py