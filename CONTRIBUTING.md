# Contributing to University Domains List

First off, thank you for taking the time to contribute! This project relies on the community to keep the global university data accurate and up-to-date.

## How to Contribute

### 1. Adding or Updating Data

All university data is stored in `world_universities_and_domains.json`. When adding new entries:

- **Complete Schema:** Every entry MUST have the following fields:
  - `name`: Official name of the university (see naming rules below).
  - `country`: Full country name in English, following [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1) English short names (e.g., `"Germany"`, not `"Deutschland"`).
  - `alpha_two_code`: Standard ISO 3166-1 alpha-2 code (e.g., `"US"`, `"TR"`).
  - `domains`: An array of strings (even if there is only one).
  - `web_pages`: An array of strings (even if there is only one). Must begin with `https://` (preferred). Only use `http://` if the university's site does not support HTTPS. Must end with a trailing slash (e.g., `https://www.boun.edu.tr/`).
  - `state-province`: State or province name in English. Use `null` if not applicable.
- **Accuracy:** Ensure the domains and web pages are currently active.
- **No Duplicates:** Check if the university already exists under a different name or variation.

### University Name Rules (`name` field)

**Latin-alphabet languages** (French, German, Spanish, Turkish, Portuguese, etc.):
Use the official name in the original language, including native characters.

```text
"Boğaziçi University"         ✓  (not "Bogazici University")
"Université Paris-Saclay"     ✓  (not "University of Paris-Saclay")
"Technische Universität Wien" ✓  (not "Vienna University of Technology")
```

**Non-Latin-script languages** (Arabic, Chinese, Japanese, Korean, Cyrillic, etc.):
Use the official English name. If no official English name exists, use a standard romanized transliteration.

```text
"Peking University"           ✓  (not "北京大学")
"King Abdulaziz University"   ✓  (not "جامعة الملك عبدالعزيز")
"Moscow State University"     ✓  (not "Московский государственный университет")
```

> **Note on consistency:** If you are fixing an existing entry that uses ASCII instead of the correct native characters (e.g., `"Ataturk University"` instead of `"Atatürk University"`), correcting it is welcome — just note the fix in your PR description.

**Note on character encoding:** Native characters (ü, ö, ğ, é, etc.) are valid UTF-8 and work fine in JSON. However, applications consuming this data that do exact string matching may miss results if they search with ASCII equivalents (e.g., searching `"Ataturk"` won't match `"Atatürk"`). API consumers should apply Unicode normalization on their side when doing name lookups.

### 2. Example Entry

```json
{
  "name": "Boğaziçi University",
  "domains": ["boun.edu.tr"],
  "web_pages": ["https://www.boun.edu.tr/"],
  "country": "Turkey",
  "alpha_two_code": "TR",
  "state-province": null
}
```

> **⚠️ CRITICAL: ROOT DOMAINS ONLY**
> Some universities use formats like `[user]@[department].[domain]`. This list MUST only contain the `[domain]` portion.
>
> - **Correct:** `usc.edu`, `itu.edu.tr`, `ox.ac.uk`
> - **Incorrect:** `cs.usc.edu`, `ogr.itu.edu.tr`, `mail.ox.ac.uk`
>
> Pull Requests containing subdomains will automatically fail the CI/CD checks.

### 3. Pull Request Process

1.  Fork the repository and create your branch from `master`.
2.  Update the JSON file.
3.  Ensure your JSON is valid.
4.  Submit the PR using the provided template.

Thank you for keeping the data clean!
