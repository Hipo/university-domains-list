import os
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


def analyze_diff(diff_text):
    if "world_universities_and_domains.json" not in diff_text:
        print("⏭️ No changes detected in the university database. Skipping review.")
        return None

    prompt = f"""
    You are an expert maintainer for an open-source global university database.
    Review the following git diff for a Pull Request:

    ```diff
    {diff_text}
    ```

    Evaluate ONLY the newly added lines (starting with '+') against our STRICT rules:
    1. **Existence**: Is it a real, recognized university?
    2. **Schema**: Does it have `name`, `country`, `alpha_two_code`, `domains`, `web_pages`, `state-province`?
    3. **ROOT DOMAINS ONLY**: Subdomains (like cs.usc.edu) are strictly forbidden.
    4. **Formatting**: Valid JSON format?

    Format your output as a clear checklist. Conclude with either "✅ PASSED" or "❌ FLAGGED: [Reason]".
    """

    for attempt in range(3):
        try:
            print(f"🧠 Sending prompt to Gemini AI (attempt {attempt + 1}/3)...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            print("✅ Gemini successfully generated a response.")
            return f"🤖 **AIOps Comprehensive PR Review**\n\n{response.text}\n\n---\n*Note: Automated review based on repository contribution guidelines.*"
        except Exception as e:
            print(f"⚠️ Gemini API Error (attempt {attempt + 1}/3): {str(e)}")
            if attempt < 2:
                time.sleep(10)

    print("⚠️ Gemini unavailable after 3 attempts. Skipping review.")
    return None


if __name__ == "__main__":
    diff = get_pr_diff()
    if diff:
        report = analyze_diff(diff)
        if report:
            post_comment(report)
