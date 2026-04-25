## Description

This PR proposes changes/additions to the university database.

## Data Completeness Checklist

- [ ] **Full Schema:** Does every entry include `name`, `country`, `domains`, `web_pages`, and `alpha_two_code`?
- [ ] **State/Province:** If applicable, is the `state-province` field filled? (If not available, ensure the field exists as `null`).
- [ ] **Data Accuracy:** Have you verified the official site and domain?
- [ ] **No Duplicates:** Have you searched the file to ensure this entry doesn't already exist?
- [ ] **Root Domain Only:** Does the `domains` array contain ONLY root domains? (e.g., `usc.edu` is correct, `cs.usc.edu` or `mail.usc.edu` is WRONG).

## Technical Checks

- [ ] JSON is valid and correctly formatted.
- [ ] No trailing commas or syntax errors.

**Note:** Please ensure all fields are present for every entry to maintain data integrity.
