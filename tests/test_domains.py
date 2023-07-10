import json
import unittest

import validators


class DomainsTests(unittest.TestCase):
    def setUp(self):
        """Load the JSON file into a variable"""
        with open("world_universities_and_domains.json", encoding="utf-8") as json_file:
            self.valid_json = json.load(json_file)

    def test_university_json_structure(self):
        """Test the structure of each university entry in the JSON file"""
        for university in self.valid_json:
            # Name
            self.assertIn("name", university, msg="University Name is missing")
            self.assertIsInstance(
                university["name"],
                (str, type(None)),
                msg="University Name must be a string or null",
            )
            # Domains
            self.assertIn("domains", university, msg="University Domains are missing")
            self.assertIsInstance(
                university["domains"],
                (list, type(None)),
                msg="University Domains must be a list or null",
            )
            if university["domains"] is not None:
                for domain in university["domains"]:
                    self.assertIsInstance(
                        domain,
                        (str, type(None)),
                        msg="University Domain must be a string or null",
                    )
                    if domain is not None:
                        self.assertTrue(
                            validators.domain(domain), msg=f"Invalid domain: {domain}"
                        )
            # Web Pages
            self.assertIn(
                "web_pages", university, msg="University Web Pages are missing"
            )
            self.assertIsInstance(
                university["web_pages"],
                (list, type(None)),
                msg="University Web Pages must be a list or null",
            )
            if university["web_pages"] is not None:
                for web_page in university["web_pages"]:
                    self.assertIsInstance(
                        web_page,
                        (str, type(None)),
                        msg="University Web Page must be a string or null",
                    )
                    if web_page is not None:
                        self.assertTrue(
                            validators.url(web_page),
                            msg=f"Invalid web page: {web_page}",
                        )
            # Alpha Two Code
            self.assertIn(
                "alpha_two_code", university, msg="Country Alpha Two Code is missing"
            )
            self.assertIsInstance(
                university["alpha_two_code"],
                (str, type(None)),
                msg="Country Alpha Two Code must be a string or null",
            )
            if university["alpha_two_code"] is not None:
                self.assertEqual(
                    len(university["alpha_two_code"]),
                    2,
                    msg=f"Country Alpha Two Code must be 2 characters long: {university['alpha_two_code']}",
                )
            # State/Province
            self.assertIn(
                "state-province", university, msg="University State/Province is missing"
            )
            self.assertIsInstance(
                university["state-province"],
                (str, type(None)),
                msg="University State/Province must be a string or null",
            )
            # Country
            self.assertIn("country", university, msg="University Country is missing")
            self.assertIsInstance(
                university["country"],
                (str, type(None)),
                msg="University Country must be a string or null",
            )


# Run tests locally
# if __name__ == "__main__":
#     unittest.main()
