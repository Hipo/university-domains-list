import unittest

from filter import _country_filter, country_filter

SAMPLE = [
    {
        "name": "MIT",
        "country": "United States",
        "domains": ["mit.edu"],
        "web_pages": [],
        "alpha_two_code": "US",
        "state-province": None,
    },
    {
        "name": "Harvard",
        "country": "United States",
        "domains": ["harvard.edu"],
        "web_pages": [],
        "alpha_two_code": "US",
        "state-province": None,
    },
    {
        "name": "Oxford",
        "country": "United Kingdom",
        "domains": ["ox.ac.uk"],
        "web_pages": [],
        "alpha_two_code": "GB",
        "state-province": None,
    },
    {
        "name": "METU",
        "country": "Turkiye",
        "domains": ["metu.edu.tr"],
        "web_pages": [],
        "alpha_two_code": "TR",
        "state-province": None,
    },
]


class CountryFilterTests(unittest.TestCase):
    def test_single_country(self):
        result = country_filter(SAMPLE, "United States")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(u["country"] == "United States" for u in result))

    def test_multiple_countries(self):
        result = country_filter(SAMPLE, ["United States", "United Kingdom"])
        self.assertEqual(len(result), 3)

    def test_case_insensitive_lower(self):
        result = country_filter(SAMPLE, "united states")
        self.assertEqual(len(result), 2)

    def test_case_insensitive_upper(self):
        result = country_filter(SAMPLE, "UNITED STATES")
        self.assertEqual(len(result), 2)

    def test_no_match(self):
        result = country_filter(SAMPLE, "Germany")
        self.assertEqual(result, [])

    def test_empty_list(self):
        result = country_filter(SAMPLE, [])
        self.assertEqual(result, [])

    def test_multiple_countries_list_order(self):
        result = country_filter(SAMPLE, ["Turkiye", "United Kingdom"])
        names = [u["name"] for u in result]
        self.assertIn("METU", names)
        self.assertIn("Oxford", names)
        self.assertEqual(len(result), 2)

    def test_internal_single_country(self):
        result = _country_filter(SAMPLE, "Turkiye", [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "METU")


if __name__ == "__main__":
    unittest.main()
