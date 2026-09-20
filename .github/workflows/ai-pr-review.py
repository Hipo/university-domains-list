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


def get_file_diff_section(diff_text, filename):
    marker = f"diff --git a/{filename} b/{filename}"
    start = diff_text.find(marker)
    if start == -1:
        return ""
    end = diff_text.find("\ndiff --git ", start + 1)
    return diff_text[start:] if end == -1 else diff_text[start:end]


def extract_touched_entries(diff_text, filename="world_universities_and_domains.json"):
    # Rebuild each JSON object's post-patch content (context '  ' lines plus
    # added '+' lines, dropping removed '-' lines) so fields keep their entry
    # grouping even when only one field of an existing entry was edited —
    # a flat per-line scan (like extract_diff_values above) can't do that
    # since alpha_two_code and country may be several lines apart and in
    # either order.
    entries = []
    current_lines, current_touched, in_object = [], False, False
    for line in get_file_diff_section(diff_text, filename).splitlines():
        if line.startswith("@@"):
            current_lines, current_touched, in_object = [], False, False
            continue
        if line.startswith(("diff --git", "index ", "--- ", "+++ ")):
            continue
        if not line or line[0] not in " +-":
            continue
        prefix, content = line[0], line[1:]
        if prefix == "-":
            continue
        stripped = content.strip()
        if stripped == "{":
            current_lines, current_touched, in_object = [], False, True
            continue
        if stripped in ("},", "}"):
            if in_object and current_touched:
                entries.append("\n".join(current_lines))
            current_lines, current_touched, in_object = [], False, False
            continue
        if in_object:
            current_lines.append(content)
            current_touched = current_touched or prefix == "+"
    return entries


def extract_field(entry_text, field):
    m = re.search(rf'"{field}"\s*:\s*"([^"]*)"', entry_text)
    return m.group(1) if m else None


# Fallback only: used when a PR's alpha_two_code has never appeared in the
# database before, so there's no existing usage to check self-consistency
# against (see find_country_code_mismatches). Sets list the ISO 3166-1
# English short name plus common accepted variants, not every possible
# spelling.
ISO_3166_ALPHA2_COUNTRIES = {
    "AD": {"Andorra"},
    "AE": {"United Arab Emirates"},
    "AF": {"Afghanistan"},
    "AG": {"Antigua and Barbuda"},
    "AI": {"Anguilla"},
    "AL": {"Albania"},
    "AM": {"Armenia"},
    "AO": {"Angola"},
    "AQ": {"Antarctica"},
    "AR": {"Argentina"},
    "AS": {"American Samoa"},
    "AT": {"Austria"},
    "AU": {"Australia"},
    "AW": {"Aruba"},
    "AX": {"Åland Islands"},
    "AZ": {"Azerbaijan"},
    "BA": {"Bosnia and Herzegovina"},
    "BB": {"Barbados"},
    "BD": {"Bangladesh"},
    "BE": {"Belgium"},
    "BF": {"Burkina Faso"},
    "BG": {"Bulgaria"},
    "BH": {"Bahrain"},
    "BI": {"Burundi"},
    "BJ": {"Benin"},
    "BL": {"Saint Barthélemy"},
    "BM": {"Bermuda"},
    "BN": {"Brunei", "Brunei Darussalam"},
    "BO": {"Bolivia", "Plurinational State of Bolivia"},
    "BQ": {"Bonaire, Sint Eustatius and Saba"},
    "BR": {"Brazil"},
    "BS": {"Bahamas"},
    "BT": {"Bhutan"},
    "BV": {"Bouvet Island"},
    "BW": {"Botswana"},
    "BY": {"Belarus"},
    "BZ": {"Belize"},
    "CA": {"Canada"},
    "CC": {"Cocos (Keeling) Islands"},
    "CD": {"Democratic Republic of the Congo", "DR Congo"},
    "CF": {"Central African Republic"},
    "CG": {"Congo", "Republic of the Congo"},
    "CH": {"Switzerland"},
    "CI": {"Côte d'Ivoire", "Ivory Coast", "Cote d'Ivoire"},
    "CK": {"Cook Islands"},
    "CL": {"Chile"},
    "CM": {"Cameroon"},
    "CN": {"China"},
    "CO": {"Colombia"},
    "CR": {"Costa Rica"},
    "CU": {"Cuba"},
    "CV": {"Cabo Verde", "Cape Verde"},
    "CW": {"Curaçao"},
    "CX": {"Christmas Island"},
    "CY": {"Cyprus"},
    "CZ": {"Czech Republic", "Czechia"},
    "DE": {"Germany"},
    "DJ": {"Djibouti"},
    "DK": {"Denmark"},
    "DM": {"Dominica"},
    "DO": {"Dominican Republic"},
    "DZ": {"Algeria"},
    "EC": {"Ecuador"},
    "EE": {"Estonia"},
    "EG": {"Egypt"},
    "EH": {"Western Sahara"},
    "ER": {"Eritrea"},
    "ES": {"Spain"},
    "ET": {"Ethiopia"},
    "FI": {"Finland"},
    "FJ": {"Fiji"},
    "FK": {"Falkland Islands"},
    "FM": {"Micronesia", "Federated States of Micronesia"},
    "FO": {"Faroe Islands"},
    "FR": {"France"},
    "GA": {"Gabon"},
    "GB": {"United Kingdom"},
    "GD": {"Grenada"},
    "GE": {"Georgia"},
    "GF": {"French Guiana"},
    "GG": {"Guernsey"},
    "GH": {"Ghana"},
    "GI": {"Gibraltar"},
    "GL": {"Greenland"},
    "GM": {"Gambia"},
    "GN": {"Guinea"},
    "GP": {"Guadeloupe"},
    "GQ": {"Equatorial Guinea"},
    "GR": {"Greece"},
    "GS": {"South Georgia and the South Sandwich Islands"},
    "GT": {"Guatemala"},
    "GU": {"Guam"},
    "GW": {"Guinea-Bissau"},
    "GY": {"Guyana"},
    "HK": {"Hong Kong"},
    "HM": {"Heard Island and McDonald Islands"},
    "HN": {"Honduras"},
    "HR": {"Croatia"},
    "HT": {"Haiti"},
    "HU": {"Hungary"},
    "ID": {"Indonesia"},
    "IE": {"Ireland"},
    "IL": {"Israel"},
    "IM": {"Isle of Man"},
    "IN": {"India"},
    "IO": {"British Indian Ocean Territory"},
    "IQ": {"Iraq"},
    "IR": {"Iran", "Islamic Republic of Iran"},
    "IS": {"Iceland"},
    "IT": {"Italy"},
    "JE": {"Jersey"},
    "JM": {"Jamaica"},
    "JO": {"Jordan"},
    "JP": {"Japan"},
    "KE": {"Kenya"},
    "KG": {"Kyrgyzstan"},
    "KH": {"Cambodia"},
    "KI": {"Kiribati"},
    "KM": {"Comoros"},
    "KN": {"Saint Kitts and Nevis"},
    "KP": {"North Korea", "Democratic People's Republic of Korea"},
    "KR": {"South Korea", "Republic of Korea"},
    "KW": {"Kuwait"},
    "KY": {"Cayman Islands"},
    "KZ": {"Kazakhstan"},
    "LA": {"Laos", "Lao People's Democratic Republic"},
    "LB": {"Lebanon"},
    "LC": {"Saint Lucia"},
    "LI": {"Liechtenstein"},
    "LK": {"Sri Lanka"},
    "LR": {"Liberia"},
    "LS": {"Lesotho"},
    "LT": {"Lithuania"},
    "LU": {"Luxembourg"},
    "LV": {"Latvia"},
    "LY": {"Libya"},
    "MA": {"Morocco"},
    "MC": {"Monaco"},
    "MD": {"Moldova", "Republic of Moldova"},
    "ME": {"Montenegro"},
    "MF": {"Saint Martin"},
    "MG": {"Madagascar"},
    "MH": {"Marshall Islands"},
    "MK": {"North Macedonia", "Macedonia"},
    "ML": {"Mali"},
    "MM": {"Myanmar", "Burma"},
    "MN": {"Mongolia"},
    "MO": {"Macao"},
    "MP": {"Northern Mariana Islands"},
    "MQ": {"Martinique"},
    "MR": {"Mauritania"},
    "MS": {"Montserrat"},
    "MT": {"Malta"},
    "MU": {"Mauritius"},
    "MV": {"Maldives"},
    "MW": {"Malawi"},
    "MX": {"Mexico"},
    "MY": {"Malaysia"},
    "MZ": {"Mozambique"},
    "NA": {"Namibia"},
    "NC": {"New Caledonia"},
    "NE": {"Niger"},
    "NF": {"Norfolk Island"},
    "NG": {"Nigeria"},
    "NI": {"Nicaragua"},
    "NL": {"Netherlands"},
    "NO": {"Norway"},
    "NP": {"Nepal"},
    "NR": {"Nauru"},
    "NU": {"Niue"},
    "NZ": {"New Zealand"},
    "OM": {"Oman"},
    "PA": {"Panama"},
    "PE": {"Peru"},
    "PF": {"French Polynesia"},
    "PG": {"Papua New Guinea"},
    "PH": {"Philippines"},
    "PK": {"Pakistan"},
    "PL": {"Poland"},
    "PM": {"Saint Pierre and Miquelon"},
    "PN": {"Pitcairn"},
    "PR": {"Puerto Rico"},
    "PS": {"Palestine", "State of Palestine"},
    "PT": {"Portugal"},
    "PW": {"Palau"},
    "PY": {"Paraguay"},
    "QA": {"Qatar"},
    "RE": {"Réunion"},
    "RO": {"Romania"},
    "RS": {"Serbia"},
    "RU": {"Russia", "Russian Federation"},
    "RW": {"Rwanda"},
    "SA": {"Saudi Arabia"},
    "SB": {"Solomon Islands"},
    "SC": {"Seychelles"},
    "SD": {"Sudan"},
    "SE": {"Sweden"},
    "SG": {"Singapore"},
    "SH": {"Saint Helena, Ascension and Tristan da Cunha"},
    "SI": {"Slovenia"},
    "SJ": {"Svalbard and Jan Mayen"},
    "SK": {"Slovakia"},
    "SL": {"Sierra Leone"},
    "SM": {"San Marino"},
    "SN": {"Senegal"},
    "SO": {"Somalia"},
    "SR": {"Suriname"},
    "SS": {"South Sudan"},
    "ST": {"Sao Tome and Principe"},
    "SV": {"El Salvador"},
    "SX": {"Sint Maarten"},
    "SY": {"Syria", "Syrian Arab Republic"},
    "SZ": {"Eswatini", "Swaziland"},
    "TC": {"Turks and Caicos Islands"},
    "TD": {"Chad"},
    "TF": {"French Southern Territories"},
    "TG": {"Togo"},
    "TH": {"Thailand"},
    "TJ": {"Tajikistan"},
    "TK": {"Tokelau"},
    "TL": {"Timor-Leste", "East Timor"},
    "TM": {"Turkmenistan"},
    "TN": {"Tunisia"},
    "TO": {"Tonga"},
    "TR": {"Turkey", "Türkiye", "Turkiye"},
    "TT": {"Trinidad and Tobago"},
    "TV": {"Tuvalu"},
    "TW": {"Taiwan"},
    "TZ": {"Tanzania", "United Republic of Tanzania"},
    "UA": {"Ukraine"},
    "UG": {"Uganda"},
    "UM": {"United States Minor Outlying Islands"},
    "US": {"United States", "United States of America"},
    "UY": {"Uruguay"},
    "UZ": {"Uzbekistan"},
    "VA": {"Vatican City", "Holy See"},
    "VC": {"Saint Vincent and the Grenadines"},
    "VE": {"Venezuela", "Bolivarian Republic of Venezuela"},
    "VG": {"British Virgin Islands"},
    "VI": {"United States Virgin Islands"},
    "VN": {"Vietnam", "Viet Nam"},
    "VU": {"Vanuatu"},
    "WF": {"Wallis and Futuna"},
    "WS": {"Samoa"},
    "YE": {"Yemen"},
    "YT": {"Mayotte"},
    "ZA": {"South Africa"},
    "ZM": {"Zambia"},
    "ZW": {"Zimbabwe"},
    # Not an official ISO 3166-1 code, but a widely used user-assigned one
    # for Kosovo (already present in this dataset).
    "XK": {"Kosovo"},
}


def find_country_code_mismatches(diff_text):
    # Primary check is self-consistency against the current database — it
    # already tolerates this dataset's real naming variants (e.g. both
    # "Vietnam" and "Viet Nam" are paired with "VN"), so it flags an actual
    # code/name mismatch without fighting existing usage. The ISO table
    # above is only a fallback for a code the dataset has never used before.
    try:
        with open("world_universities_and_domains.json", "r", encoding="utf-8") as f:
            base_entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    alpha_to_countries, country_to_alphas = {}, {}
    for entry in base_entries:
        code, country = entry.get("alpha_two_code"), entry.get("country")
        if code and country:
            alpha_to_countries.setdefault(code, set()).add(country)
            country_to_alphas.setdefault(country, set()).add(code)

    warnings = []
    for entry_text in extract_touched_entries(diff_text):
        code = extract_field(entry_text, "alpha_two_code")
        country = extract_field(entry_text, "country")
        if not code or not country:
            continue
        if not re.fullmatch(r"[A-Z]{2}", code):
            warnings.append(
                f'`alpha_two_code: "{code}"` is not a valid two-letter uppercase ISO 3166-1 code.'
            )
            continue
        known_countries = alpha_to_countries.get(code)
        if known_countries is not None:
            if country in known_countries:
                continue
            known_codes = country_to_alphas.get(country)
            if known_codes:
                warnings.append(
                    f'`alpha_two_code: "{code}"` does not match `country: "{country}"` — '
                    f'"{code}" is normally paired with {"/".join(sorted(known_countries))}, '
                    f'while "{country}" is normally paired with {"/".join(sorted(known_codes))}.'
                )
            else:
                warnings.append(
                    f'`country: "{country}"` has never been used with `alpha_two_code: "{code}"` before '
                    f'(existing entries use {"/".join(sorted(known_countries))} for "{code}") — please double-check.'
                )
            continue

        # Code never used in this dataset before — fall back to the
        # canonical ISO 3166-1 table instead of skipping the check entirely.
        canonical_names = ISO_3166_ALPHA2_COUNTRIES.get(code)
        if canonical_names is None:
            warnings.append(
                f'`alpha_two_code: "{code}"` is not a recognized ISO 3166-1 alpha-2 code.'
            )
        elif country not in canonical_names:
            warnings.append(
                f'`alpha_two_code: "{code}"` is new to this database and does not match `country: "{country}"` '
                f'— the ISO 3166-1 name for "{code}" is {"/".join(sorted(canonical_names))}.'
            )
    return warnings


def format_warnings_section(title, warnings):
    body = "\n".join(f"- {w}" for w in warnings)
    return f"⚠️ **{title}:**\n{body}"


def build_deterministic_report(checks):
    return "\n\n".join(
        format_warnings_section(title, warnings)
        for title, warnings in checks.items()
        if warnings
    )


def build_rules_addendum(checks):
    parts = []
    for title, warnings in checks.items():
        if not warnings:
            continue
        wlist = "\n".join(f"    - {w}" for w in warnings)
        parts.append(f"""
    {title.upper()} RESULTS (computed against the current database — treat these as verified facts, not suggestions to re-check):
{wlist}
""")
    if parts:
        parts.append(
            '\n    Any entry flagged above MUST cause the review to conclude "❌ FLAGGED".\n'
        )
    return "".join(parts)


def analyze_diff(diff_text):
    if "world_universities_and_domains.json" not in diff_text:
        print("⏭️ No changes detected in the university database. Skipping review.")
        return None

    checks = {
        "Duplicate check": find_duplicates(diff_text),
        "Country / alpha_two_code check": find_country_code_mismatches(diff_text),
    }

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

    rules_section += build_rules_addendum(checks)

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
            deterministic_report = build_deterministic_report(checks)
            if deterministic_report:
                report += f"\n\n{deterministic_report}"
            report += "\n\n---\n*Note: Automated review based on repository contribution guidelines.*"
            return report
        # Retry loop must survive any SDK/network failure from the Gemini call.
        except Exception as e:  # noqa: BLE001
            print(f"⚠️ Gemini API Error (attempt {attempt + 1}/3): {e!s}")
            if attempt < 2:
                time.sleep(10)

    print("⚠️ Gemini unavailable after 3 attempts.")
    deterministic_report = build_deterministic_report(checks)
    if deterministic_report:
        return (
            "🤖 **AIOps Comprehensive PR Review**\n\n"
            "Gemini was unavailable, but automated checks against the current database found:\n\n"
            f"{deterministic_report}\n\n"
            "❌ FLAGGED: see automated checks above.\n\n"
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
