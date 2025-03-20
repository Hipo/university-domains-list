import json
import unittest

import validators


class DomainsTests(unittest.TestCase):
    def setUp(self):
        """Load the JSON file into a variable"""
        # Using a relative path that works regardless of where the test is run from
        import os

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(
            os.path.dirname(script_dir), "world_universities_and_domains.json"
        )

        with open(json_path, encoding="utf-8") as json_file:
            self.valid_json = json.load(json_file)

    def test_trimmed_fields(self):
        """Test that all string fields in each university entry are properly trimmed"""
        for university in self.valid_json:
            # Check university name
            if isinstance(university["name"], str):
                self.assertEqual(
                    university["name"],
                    university["name"].strip(),
                    msg=f"University Name contains leading/trailing whitespace: '{university['name']}'",
                )

            # Check domains
            if university["domains"] is not None:
                for domain in university["domains"]:
                    if isinstance(domain, str):
                        self.assertEqual(
                            domain,
                            domain.strip(),
                            msg=f"Domain contains leading/trailing whitespace: '{domain}'",
                        )

            # Check web_pages
            if university["web_pages"] is not None:
                for web_page in university["web_pages"]:
                    if isinstance(web_page, str):
                        self.assertEqual(
                            web_page,
                            web_page.strip(),
                            msg=f"Web page contains leading/trailing whitespace: '{web_page}'",
                        )

            # Check country
            if isinstance(university["country"], str):
                self.assertEqual(
                    university["country"],
                    university["country"].strip(),
                    msg=f"Country contains leading/trailing whitespace: '{university['country']}'",
                )

            # Check alpha_two_code
            if isinstance(university["alpha_two_code"], str):
                self.assertEqual(
                    university["alpha_two_code"],
                    university["alpha_two_code"].strip(),
                    msg=f"Alpha two code contains leading/trailing whitespace: '{university['alpha_two_code']}'",
                )

            # Check state-province
            if isinstance(university["state-province"], str):
                self.assertEqual(
                    university["state-province"],
                    university["state-province"].strip(),
                    msg=f"State/Province contains leading/trailing whitespace: '{university['state-province']}'",
                )


# Run tests locally
# if __name__ == "__main__":
#    unittest.main()
