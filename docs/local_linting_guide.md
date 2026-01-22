# Local Linting Guide

This guide explains how to run the same linting checks locally that are used in the GitHub Actions CI pipeline.

## Prerequisites

Make sure you have Python installed and create a virtual environment:

```bash
# Create a virtual environment (if not already created)
python -m venv venv

# Activate the environment
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows
```

## Install Required Tools

Install all the linting tools used in the CI pipeline:

```bash
# Install Python linting tools
pip install black isort

# Install Node.js tools (requires Node.js to be installed)
npm install -g jsonlint
```

## Linting Commands

### 1. Python Code Formatting (Black)

Check if Python files need formatting:
```bash
black --check .
```

Auto-format Python files:
```bash
black .
```

Check specific files:
```bash
black --check tests/test_trimming.py filter.py
```

### 2. Python Import Sorting (isort)

Check import sorting:
```bash
isort --check-only .
```

Auto-fix import sorting:
```bash
isort .
```

### 3. JSON Validation

Validate JSON files:
```bash
jsonlint world_universities_and_domains.json
```

## GitHub Actions Compatibility

The local commands above mirror exactly what GitHub Actions runs:
- `black --check .` (same as GitHub Actions)
- `isort --check-only .` (same as GitHub Actions)  
- `jsonlint world_universities_and_domains.json` (same as GitHub Actions)
