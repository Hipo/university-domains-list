import unittest

from base_test import BaseUniversityTest


class DuplicateTests(BaseUniversityTest):
    def test_no_duplicate_entries(self):
        """Test that no two entries share both a domain and a web page"""
        errors = []
        data = self.valid_json
        for i, a in enumerate(data):
            for b in data[i + 1 :]:
                shared_domains = set(a.get("domains") or []) & set(
                    b.get("domains") or []
                )
                shared_pages = set(a.get("web_pages") or []) & set(
                    b.get("web_pages") or []
                )
                if shared_domains and shared_pages:
                    errors.append(
                        f"Duplicate: '{a['name']}' / '{b['name']}'"
                        f" — shared domains: {shared_domains}"
                    )
        if errors:
            self.fail("\n".join(errors))


if __name__ == "__main__":
    unittest.main()
