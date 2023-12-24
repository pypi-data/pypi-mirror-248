#!/bin/bash

# Create and activate virtual environment
python -m venv --clear --prompt='cookiecutter-python-vscode-github' .venv
source .venv/bin/activate
# Install development dependencies
make -B install
# Config pre-commit
pre-commit install --overwrite --hook-type=pre-commit --hook-type=pre-push
