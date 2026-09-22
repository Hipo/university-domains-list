"""Advisory, non-blocking check for domains added or removed in a PR.

For every domain that a PR adds to or removes from
world_universities_and_domains.json, this looks up whether the domain
still resolves (A/AAAA) and still accepts mail (MX), and posts the
result as a PR comment. It never fails the workflow: a domain that
looks dead, or one that looks surprisingly alive, is useful context for
a human reviewer, not something a bot should block on.
"""

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
import requests

PR_NUMBER = os.environ.get("PR_NUMBER")
REPO = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

DNS_TIMEOUT_SECS = 5
FILENAME = "world_universities_and_domains.json"


def get_pr_diff():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch diff: {response.status_code} - {response.text}")
        return ""
    return response.text


def post_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers, json={"body": comment}, timeout=30)
    if response.status_code != 201:
        print(f"⚠️ Failed to post comment: {response.status_code} - {response.text}")
    else:
        print("✅ Comment posted!")


def normalize_domain(domain):
    return domain.strip().lower().removeprefix("www.")


def get_file_diff_section(diff_text, filename):
    marker = f"diff --git a/{filename} b/{filename}"
    start = diff_text.find(marker)
    if start == -1:
        return ""
    end = diff_text.find("\ndiff --git ", start + 1)
    return diff_text[start:] if end == -1 else diff_text[start:end]


def extract_domain_diff(diff_text):
    """Return (added, removed) domain sets, edits to other fields excluded.

    Only lines inside a "domains" array count — a domain untouched by the
    PR never shows up as a +/- line in the first place, so no separate
    JSON parse is needed to tell "changed" from "unchanged".
    """
    added, removed = set(), set()
    for line in get_file_diff_section(diff_text, FILENAME).splitlines():
        if (
            '"domains"' not in line
            or line[:1] not in "+-"
            or line.startswith(("+++", "---"))
        ):
            continue
        values = {
            normalize_domain(d)
            for d in re.findall(r'"([^"]+)"', line.split('"domains"', 1)[1])
        }
        (added if line[0] == "+" else removed).update(values)
    # A domain present on both sides is a reformat/no-op, not a real change.
    return added - removed, removed - added


def check_domain(domain):
    resolver = dns.resolver.Resolver()
    resolver.timeout = DNS_TIMEOUT_SECS
    resolver.lifetime = DNS_TIMEOUT_SECS

    resolves, has_mx, note = False, False, None
    for rtype in ("A", "AAAA"):
        try:
            resolver.resolve(domain, rtype)
            resolves = True
            break
        except dns.resolver.NXDOMAIN:
            note = "NXDOMAIN"
        except dns.resolver.NoAnswer:
            continue
        except Exception as e:  # noqa: BLE001 - any resolver failure is just "unknown"
            note = type(e).__name__

    try:
        resolver.resolve(domain, "MX")
        has_mx = True
    except Exception as e:  # noqa: BLE001 - absence of MX is normal, not an error
        print(f"   (no MX for {domain}: {type(e).__name__})")

    return {"domain": domain, "resolves": resolves, "has_mx": has_mx, "note": note}


def format_result(result, *, flag_if_alive):
    domain, resolves, has_mx = result["domain"], result["resolves"], result["has_mx"]
    status = []
    status.append(
        "resolves"
        if resolves
        else f"does NOT resolve ({result['note'] or 'no A/AAAA'})"
    )
    status.append("has MX" if has_mx else "no MX")
    alive = resolves or has_mx

    if flag_if_alive and alive:
        return f"- ⚠️ `{domain}` — {', '.join(status)}. Still appears active — please confirm this removal is intentional."
    if not flag_if_alive and not alive:
        return f"- ⚠️ `{domain}` — {', '.join(status)}. Double-check this is a real, currently-live domain."
    return f"- ✅ `{domain}` — {', '.join(status)}."


def build_report(added, removed):
    with ThreadPoolExecutor(max_workers=8) as pool:
        added_results = list(pool.map(check_domain, sorted(added)))
        removed_results = list(pool.map(check_domain, sorted(removed)))

    sections = []
    if added_results:
        lines = "\n".join(format_result(r, flag_if_alive=False) for r in added_results)
        sections.append(f"**Newly added domains:**\n{lines}")
    if removed_results:
        lines = "\n".join(format_result(r, flag_if_alive=True) for r in removed_results)
        sections.append(f"**Removed domains:**\n{lines}")

    body = "\n\n".join(sections)
    return (
        "🌐 **Domain Status Check** (advisory only — does not block this PR)\n\n"
        f"{body}\n\n"
        "---\n*A flagged removed domain may still be receiving real mail traffic even if "
        "no longer the university's primary domain — consider keeping it as a secondary "
        "entry in `domains` instead of dropping it.*"
    )


def main():
    if not all([PR_NUMBER, REPO, GITHUB_TOKEN]):
        print("⚠️ Missing PR_NUMBER, GITHUB_REPOSITORY, or GITHUB_TOKEN — skipping.")
        return

    diff = get_pr_diff()
    if FILENAME not in diff:
        print(f"⏭️ No changes to {FILENAME}. Skipping.")
        return

    added, removed = extract_domain_diff(diff)
    if not added and not removed:
        print("⏭️ No domain additions or removals in this diff. Skipping.")
        return

    report = build_report(added, removed)
    post_comment(report)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001 - this check must never fail the workflow
        print(f"⚠️ Domain status check hit an unexpected error, skipping: {e!s}")
        sys.exit(0)
