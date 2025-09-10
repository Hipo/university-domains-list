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
        errors = []
        
        for i, university in enumerate(self.valid_json):
            # Check university name
            if isinstance(university["name"], str):
                original_name = university["name"]
                trimmed_name = original_name.strip()
                if original_name != trimmed_name:
                    errors.append(f"Entry {i}: University Name contains leading/trailing whitespace: '{original_name}' -> should be '{trimmed_name}'")

            # Check domains
            if university["domains"] is not None:
                for j, domain in enumerate(university["domains"]):
                    if isinstance(domain, str):
                        original_domain = domain
                        trimmed_domain = original_domain.strip()
                        if original_domain != trimmed_domain:
                            errors.append(f"Entry {i}: Domain {j} contains leading/trailing whitespace: '{original_domain}' -> should be '{trimmed_domain}'")

            # Check web_pages
            if university["web_pages"] is not None:
                for j, web_page in enumerate(university["web_pages"]):
                    if isinstance(web_page, str):
                        original_web_page = web_page
                        trimmed_web_page = original_web_page.strip()
                        if original_web_page != trimmed_web_page:
                            errors.append(f"Entry {i}: Web page {j} contains leading/trailing whitespace: '{original_web_page}' -> should be '{trimmed_web_page}'")

            # Check country
            if isinstance(university["country"], str):
                original_country = university["country"]
                trimmed_country = original_country.strip()
                if original_country != trimmed_country:
                    errors.append(f"Entry {i}: Country contains leading/trailing whitespace: '{original_country}' -> should be '{trimmed_country}'")

            # Check alpha_two_code
            if isinstance(university["alpha_two_code"], str):
                original_alpha = university["alpha_two_code"]
                trimmed_alpha = original_alpha.strip()
                if original_alpha != trimmed_alpha:
                    errors.append(f"Entry {i}: Alpha two code contains leading/trailing whitespace: '{original_alpha}' -> should be '{trimmed_alpha}'")

            # Check state-province
            if isinstance(university["state-province"], str):
                original_state = university["state-province"]
                trimmed_state = original_state.strip()
                if original_state != trimmed_state:
                    errors.append(f"Entry {i}: State/Province contains leading/trailing whitespace: '{original_state}' -> should be '{trimmed_state}'")

        # If there are any errors, fail the test with all error messages
        if errors:
            error_message = f"Found {len(errors)} fields with whitespace issues:\n" + "\n".join(errors[:10])  # Show first 10 errors
            if len(errors) > 10:
                error_message += f"\n... and {len(errors) - 10} more errors"
            self.fail(error_message)


# Run tests locally
# if __name__ == "__main__":
#     unittest.main()