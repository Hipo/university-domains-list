import json
import unittest

import validators


class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        with open("world_universities_and_domains.json", encoding="utf-8") as json_file:
            valid_json = json.load(json_file)
        for university in valid_json:
            self.assertIn("name", university, msg="University Name is missing")
            self.assertIn("domains", university, msg="University Domains are missing")
            self.assertIsInstance(university["domains"], list, msg="University Domains must be a list")
            for domain in university["domains"]:
                self.assertTrue(validators.domain(domain), msg=f"Invalid domain: {domain}")
            self.assertIn("web_pages", university, msg="University Web Pages are missing")
            self.assertIsInstance(university["web_pages"], list, msg="University Web Pages must be a list")
            for web_page in university["web_pages"]:
                self.assertTrue(validators.url(web_page), msg=f"Invalid web page: {web_page}")
            self.assertIn("alpha_two_code", university, msg="University Alpha Two Code is missing")
            self.assertIn("state-province", university, msg="University State/Province is missing")
            self.assertIn("country", university, msg="University Country is missing")


# Run tests locally
if __name__ == "__main__":
    unittest.main()