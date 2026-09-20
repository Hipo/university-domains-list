import json
import os
import re
import sys
import time

import requests
from google import genai

API_KEY = os.environ.get("AI_API_KEY")
PR_NUMBER = os.environ.get("PR_NUMBER")
REPO = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

print(f"🔍 DEBUG: Target PR: {PR_NUMBER}, Repository: {REPO}")

if not API_KEY:
    print("❌ CRITICAL: AI_API_KEY is missing! GitHub Secrets are not accessible.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)


def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }
    print(f"📥 Fetching diff from: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch diff: {response.status_code} - {response.text}")
        sys.exit(1)
    return response.text


def post_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    print(f"📤 Posting comment to PR #{PR_NUMBER}")
    response = requests.post(url, headers=headers, json={"body": comment})
    if response.status_code != 201:
        print(f"❌ Failed to post comment: {response.status_code} - {response.text}")
        sys.exit(1)
    print("✅ Comment successfully posted!")


def get_contributing_guide():
    try:
        with open("CONTRIBUTING.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ CONTRIBUTING.md not found, falling back to built-in rules.")
        return None


def normalize_domain(domain):
    return domain.strip().lower().removeprefix("www.")


def normalize_url(url):
    return url.strip().lower().rstrip("/")


def extract_diff_values(diff_text, prefix):
    # The diff formats domains/web_pages as single-line JSON arrays, so a
    # line-level regex is enough — no need to parse the diff into full entries.
    domains, urls = set(), set()
    for line in diff_text.splitlines():
        if not line.startswith(prefix) or line.startswith(prefix * 3):
            continue
        if '"domains"' in line:
            domains.update(re.findall(r'"([^"]+)"', line.split('"domains"', 1)[1]))
        if '"web_pages"' in line:
            urls.update(re.findall(r'"([^"]+)"', line.split('"web_pages"', 1)[1]))
    return domains, urls


def find_duplicates(diff_text):
    # Checked out at the base branch (see actions/checkout in ai-review.yml),
    # so this is the pre-PR state of the database — exactly what the diff's
    # additions need to be checked against.
    try:
        with open("world_universities_and_domains.json", "r", encoding="utf-8") as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    existing_domains, existing_urls = {}, {}
    for entry in entries:
        name = entry.get("name", "unknown")
        for d in entry.get("domains") or []:
            existing_domains[normalize_domain(d)] = name
        for u in entry.get("web_pages") or []:
            existing_urls[normalize_url(u)] = name

    added_domains, added_urls = extract_diff_values(diff_text, "+")
    removed_domains, removed_urls = extract_diff_values(diff_text, "-")

    # Exclude anything also removed in the same diff — that's an edit to an
    # existing entry, not a new duplicate.
    new_domains = {normalize_domain(d) for d in added_domains} - {
        normalize_domain(d) for d in removed_domains
    }
    new_urls = {normalize_url(u) for u in added_urls} - {
        normalize_url(u) for u in removed_urls
    }

    warnings = []
    for d in sorted(new_domains):
        if d in existing_domains:
            warnings.append(
                f'Domain `{d}` already exists in the database (used by "{existing_domains[d]}").'
            )
    for u in sorted(new_urls):
        if u in existing_urls:
            warnings.append(
                f'Web page `{u}` already exists in the database (used by "{existing_urls[u]}").'
            )
    return warnings


def analyze_diff(diff_text):
    if "world_universities_and_domains.json" not in diff_text:
        print("⏭️ No changes detected in the university database. Skipping review.")
        return None

    duplicate_warnings = find_duplicates(diff_text)

    contributing_guide = get_contributing_guide()

    if contributing_guide:
        rules_section = f"""
    The official contribution guidelines for this repository are:

    ---
    {contributing_guide}
    ---
    """
    else:
        rules_section = """
    Evaluate against these rules:
    1. **Existence**: Is it a real, recognized university?
    2. **Schema**: Does it have `name`, `country`, `alpha_two_code`, `domains`, `web_pages`, `state-province`?
    3. **ROOT DOMAINS ONLY (applies to `domains` field only)**: The `domains` array must contain only root domains — subdomains are forbidden (e.g., `usc.edu` is correct, `cs.usc.edu` is not). This rule does NOT apply to `web_pages`; `web_pages` may contain any valid URL including subdomains.
    4. **Formatting**: Valid JSON format?
    """

    if duplicate_warnings:
        duplicate_list = "\n".join(f"    - {w}" for w in duplicate_warnings)
        rules_section += f"""

    DUPLICATE CHECK RESULTS (computed by comparing this diff against the full current database — treat these as verified facts, not suggestions to re-check):
{duplicate_list}

    Any entry matching one of the above MUST cause the review to conclude "❌ FLAGGED" for being a duplicate.
    """

    prompt = f"""
    You are an expert maintainer for an open-source global university database.
    Review the following git diff for a Pull Request:

    ```diff
    {diff_text}
    ```
    {rules_section}
    Evaluate ONLY the newly added lines (starting with '+').
    Format your output as a clear checklist. Conclude with either "✅ PASSED" or "❌ FLAGGED: [Reason]".
    """

    for attempt in range(3):
        try:
            print(f"🧠 Sending prompt to Gemini AI (attempt {attempt + 1}/3)...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            print("✅ Gemini successfully generated a response.")
            report = f"🤖 **AIOps Comprehensive PR Review**\n\n{response.text}"
            if duplicate_warnings:
                dup_list = "\n".join(f"- {w}" for w in duplicate_warnings)
                report += f"\n\n⚠️ **Duplicate check (verified against current database):**\n{dup_list}"
            report += "\n\n---\n*Note: Automated review based on repository contribution guidelines.*"
            return report
        # Retry loop must survive any SDK/network failure from the Gemini call.
        except Exception as e:  # noqa: BLE001
            print(f"⚠️ Gemini API Error (attempt {attempt + 1}/3): {e!s}")
            if attempt < 2:
                time.sleep(10)

    print("⚠️ Gemini unavailable after 3 attempts.")
    if duplicate_warnings:
        dup_list = "\n".join(f"- {w}" for w in duplicate_warnings)
        return (
            "🤖 **AIOps Comprehensive PR Review**\n\n"
            "Gemini was unavailable, but an automated check against the current database found:\n\n"
            f"⚠️ **Duplicate check:**\n{dup_list}\n\n"
            "❌ FLAGGED: possible duplicate entry.\n\n"
            "---\n*Note: Automated review based on repository contribution guidelines.*"
        )
    print("Skipping review.")
    return None


if __name__ == "__main__":
    diff = get_pr_diff()
    if diff:
        report = analyze_diff(diff)
        if report:
            post_comment(report)
