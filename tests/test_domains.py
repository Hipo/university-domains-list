import json
import unittest

import validators


class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        with open(
            "world_universities_and_domains.json", encoding="utf-8"
        ) as json_file:
            valid_json = json.load(json_file)
        for university in valid_json:
            self.assertIn("name", university)
            self.assertIn("domains", university)
            self.assertIsInstance(university["domains"], list)
            for domain in university["domains"]:
                self.assertTrue(validators.domain(domain))
            self.assertIn("web_pages", university)
            self.assertIn("alpha_two_code", university)
            self.assertIn("state-province", university)
            self.assertIn("country", university)
