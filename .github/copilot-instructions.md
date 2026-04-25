# Agent Instructions

Welcome! These instructions are designed to onboard you to the `Hipo/university-domains-list` codebase. Please trust the information provided here to accomplish your tasks efficiently. Only perform exploratory searches if you encounter unexpected errors or missing context not covered in this guide.

## High-Level Details

- **Project Summary:** This repository maintains a comprehensive, open-source JSON dataset mapping the world's universities to their respective domain names, web pages, and countries. The dataset is primarily utilized by developers for email domain validation and demographic auto-generation.
- **Tech Stack & Runtimes:** The core project is purely data-centric (JSON). The repository tooling relies on Python (for validation tests and data filtering) and Prettier (Node.js ecosystem) for consistent formatting.
- **Project Size & Type:** It is a small dataset repository prioritizing accurate data entry and schema compliance over complex code compilation.

## Project Layout & Architecture

Knowing where files are located will save you from needing to use `find` or `grep`.

- **`world_universities_and_domains.json`**: The primary artifact of the project. It contains a single large JSON array of university objects. Keys for each object include `alpha_two_code`, `country`, `state-province`, `domains`, `name`, and `web_pages`.
- **`filter.py`**: A Python script in the root directory. It allows users to shrink the payload by generating a filtered JSON file containing only universities from specified countries.
- **`tests/`**: Directory containing Python scripts to validate the JSON structure, detect duplicates, and enforce schema compliance.
  - `tests/main.py`: The entry point for validating the JSON dataset.
  - `tests/requirements.txt`: Python dependencies required to run the tests.
- **`.github/workflows/`**: Contains the Continuous Integration (CI) pipelines that automatically run validation and Prettier checks on Pull Requests.
- **`.prettierrc`**: Configuration file specifying the formatting rules for Prettier.

## Build & Validation Instructions

Since this is a dataset, there is no traditional "build" compilation step. However, changes **must** be rigorously validated and formatted before proposing a pull request to avoid CI failures.

### 1. Formatting the Data

Always format the JSON file after making any edits. The CI pipeline will reject pull requests that do not strictly adhere to the project's formatting conventions.

**Command:**

```bash
npx prettier --write world_universities_and_domains.json
```

Expected Outcome: The JSON file is modified in place to enforce standard spacing, brackets, and quotes as defined by .prettierrc.

### 2. Running the Test Pipeline

Every modification or addition to the dataset must be validated locally. This script checks for schema breakages, missing fields, and duplicate domain entries.

**Sequence of Steps:**

```bash
# 1. Navigate to the tests directory
cd tests

# 2. Install validation dependencies
pip install -r requirements.txt

# 3. Run the validation suite
python main.py

# 4. Return to root when finished
cd ..
```

Preconditions: A Python 3 environment must be active.
Expected Outcome: The script should execute cleanly with no output or a success message. If python main.py throws an AssertionError or exception, review your JSON modifications.

Troubleshooting: Test failures almost always mean you introduced a duplicate domain/URL, left a mandatory field missing (such as name, country, or domains), or included trailing/leading whitespace in a string value.

### 3. Data Entry Validation Guidelines

To further ensure your modifications are accepted seamlessly, always validate your intent against these domain rules:

- **Internet Validation (If Applicable):** If you are equipped with internet access or web search capabilities, always search for the university online to validate the correctness of its name, domain, and primary web page before proposing an addition or modification. Ensure the domain actively resolves to the stated institution.
- **Root Domains Only:** Universities often use subdomains for departments or student email scopes (e.g., student@cs.usc.edu). The dataset must only contain the root domain (usc.edu).
- **No Protocols in Domains:** The domains array should consist strictly of domain names without prefixes (e.g., sabanciuniv.edu, not http://www.sabanciuniv.edu).
- **Web Pages Array:** Unlike domains, strings in the web_pages array must include the protocol (e.g., http://www.sabanciuniv.edu/).

**When to Search:** Rely strictly on the paths and commands provided here. Only use grep, find, or repository searches if the validation test suite fails due to missing files, or if the Python environment indicates missing upstream dependencies.
