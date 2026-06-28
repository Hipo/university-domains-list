import unittest
from urllib.parse import urlparse

from base_test import BaseUniversityTest


class FormatTests(BaseUniversityTest):

    def test_trimmed_fields(self):
        """Test that all string fields are free of leading/trailing whitespace"""
        errors = []
        for i, university in enumerate(self.valid_json):
            for field in ["name", "country", "alpha_two_code", "state-province"]:
                value = university.get(field)
                if isinstance(value, str) and value != value.strip():
                    errors.append(
                        f"Entry {i}: '{field}' has leading/trailing whitespace: '{value}'"
                    )

            for j, domain in enumerate(university.get("domains") or []):
                if isinstance(domain, str) and domain != domain.strip():
                    errors.append(
                        f"Entry {i}: domain[{j}] has leading/trailing whitespace: '{domain}'"
                    )

            for j, web_page in enumerate(university.get("web_pages") or []):
                if isinstance(web_page, str) and web_page != web_page.strip():
                    errors.append(
                        f"Entry {i}: web_pages[{j}] has leading/trailing whitespace: '{web_page}'"
                    )

        if errors:
            error_message = f"Found {len(errors)} whitespace issues:\n" + "\n".join(
                errors[:10]
            )
            if len(errors) > 10:
                error_message += f"\n... and {len(errors) - 10} more errors"
            self.fail(error_message)

    def test_web_pages_trailing_slash(self):
        """Test that all web_pages URLs end with a trailing slash"""
        errors = []
        for i, university in enumerate(self.valid_json):
            for j, web_page in enumerate(university.get("web_pages") or []):
                if isinstance(web_page, str) and not web_page.endswith("/"):
                    errors.append(
                        f"Entry {i} ({university['name']}): web_pages[{j}] missing trailing slash: '{web_page}'"
                    )
        if errors:
            error_message = (
                f"Found {len(errors)} URLs missing trailing slash:\n"
                + "\n".join(errors[:10])
            )
            if len(errors) > 10:
                error_message += f"\n... and {len(errors) - 10} more errors"
            self.fail(error_message)

    def test_web_pages_root_url(self):
        """Test that all web_pages URLs are root URLs (no path beyond /)"""
        errors = []
        for i, university in enumerate(self.valid_json):
            for j, web_page in enumerate(university.get("web_pages") or []):
                if not isinstance(web_page, str):
                    continue
                path = urlparse(web_page).path
                if path not in ("", "/"):
                    errors.append(
                        f"Entry {i} ({university['name']}): web_pages[{j}] must be a root URL: '{web_page}'"
                    )
        if errors:
            error_message = f"Found {len(errors)} non-root URLs:\n" + "\n".join(
                errors[:10]
            )
            if len(errors) > 10:
                error_message += f"\n... and {len(errors) - 10} more errors"
            self.fail(error_message)


if __name__ == "__main__":
    unittest.main()
