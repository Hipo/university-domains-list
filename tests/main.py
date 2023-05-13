import json
import logging
import unittest

import requests
import validators


class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        with open(
            "../world_universities_and_domains.json", encoding="utf-8"
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

    def test_check_is_alive(self):
        """ check url then if url isn't alive, add to file """
        with open(
            "../world_universities_and_domains.json", encoding="utf-8"
        ) as json_raw:
            universities = json.load(json_raw)
        dead_sites = False
        for university in universities[:]:
            try:
                for web_page in university["web_pages"]:
                    requests.head(web_page, allow_redirects=False, timeout=10.0)
            except Exception as exc:
                logging.warning("- Website doesn't exist: %s", web_page)
                logging.info("%s", exc)
                dead_sites = True
        self.assertFalse(dead_sites)


if __name__ == "__main__":
    unittest.main(verbosity=2)
