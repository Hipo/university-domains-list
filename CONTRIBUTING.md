# Contributing to University Domains List

First off, thank you for taking the time to contribute! This project relies on the community to keep the global university data accurate and up-to-date.

## How to Contribute

### 1. Adding or Updating Data

All university data is stored in `world_universities_and_domains.json`. When adding new entries:

- **Complete Schema:** Every entry MUST have the following fields:
  - `name`: Official name of the university.
  - `country`: Full country name.
  - `alpha_two_code`: Standard ISO 3166-1 alpha-2 code (e.g., "US", "TR").
  - `domains`: An array of strings (even if there is only one).
  - `web_pages`: An array of strings.
  - `state-province`: State or province name. Use `null` if not applicable.
- **Accuracy:** Ensure the domains and web pages are currently active.
- **No Duplicates:** Check if the university already exists under a different name or variation.

> **⚠️ CRITICAL: ROOT DOMAINS ONLY**
> Some universities use formats like `[user]@[department].[domain]`. This list MUST only contain the `[domain]` portion.
>
> - **Correct:** `usc.edu`, `itu.edu.tr`, `ox.ac.uk`
> - **Incorrect:** `cs.usc.edu`, `ogr.itu.edu.tr`, `mail.ox.ac.uk`
>
> Pull Requests containing subdomains will automatically fail the CI/CD checks.

### 2. Pull Request Process

1.  Fork the repository and create your branch from `master`.
2.  Update the JSON file.
3.  Ensure your JSON is valid.
4.  Submit the PR using the provided template.

Thank you for keeping the data clean!
