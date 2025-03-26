import unittest
from university-domains-list import filter


class CountryFilterTests(unittest.TestCase):
    def setUp(self):
        # Sample source data
        self.source_data = [
            {
                "name": "Kharkiv National University",
                "domains": ["student.karazin.ua", "karazin.ua"],
                "web_pages": ["https://karazin.ua"],
                "country": "Ukraine",
                "alpha_two_code": "UA",
                "state-province": None
            },
            {
                "name": "Universidad Técnica Federico Santa María",
                "domains": ["usm.cl"],
                "web_pages": ["https://usm.cl"],
                "country": "Chile",
                "alpha_two_code": "CL",
                "state-province": None
            },
            {
                "name": "IÉSEG School of Management",
                "domains": ["ieseg.fr"],
                "web_pages": ["https://ieseg.fr"],
                "country": "France",
                "alpha_two_code": "FR",
                "state-province": None
            },
            {
                "name": "Sun Yat-Sen University",
                "domains": ["mail2.sysu.edu.cn", "mail.sysu.edu.cn"],
                "web_pages": ["https://sysu.edu.cn"],
                "country": "China",
                "alpha_two_code": "CN",
                "state-province": None
            }
        ]

    def test_single_country_scope(self):
        filtered_output = country_filter(self.source_data, "China")
        expected_output = [
            {
                "name": "Sun Yat-Sen University",
                "domains": ["mail2.sysu.edu.cn", "mail.sysu.edu.cn"],
                "web_pages": ["https://sysu.edu.cn"],
                "country": "China",
                "alpha_two_code": "CN",
                "state-province": None
            }
        ]
        self.assertEqual(filtered_output, expected_output)

    def test_multiple_country_scopes(self):
        filtered_output = country_filter(self.source_data, ["China", "France"])
        expected_output = [
            {
                "name": "IÉSEG School of Management",
                "domains": ["ieseg.fr"],
                "web_pages": ["https://ieseg.fr"],
                "country": "France",
                "alpha_two_code": "FR",
                "state-province": None
            },
            {
                "name": "Sun Yat-Sen University",
                "domains": ["mail2.sysu.edu.cn", "mail.sysu.edu.cn"],
                "web_pages": ["https://sysu.edu.cn"],
                "country": "China",
                "alpha_two_code": "CN",
                "state-province": None
            }
        ]
        self.assertEqual(filtered_output, expected_output)

    def test_non_existent_country_scope(self):
        filtered_output = country_filter(self.source_data, "Germany")
        expected_output = []
        self.assertEqual(filtered_output, expected_output)

    def test_case_sensitivity(self):
        filtered_output = country_filter(self.source_data, ["CHINA", "france"])
        expected_output = [
            {
                "name": "IÉSEG School of Management",
                "domains": ["ieseg.fr"],
                "web_pages": ["https://ieseg.fr"],
                "country": "France",
                "alpha_two_code": "FR",
                "state-province": None
            },
            {
                "name": "Sun Yat-Sen University",
                "domains": ["mail2.sysu.edu.cn", "mail.sysu.edu.cn"],
                "web_pages": ["https://sysu.edu.cn"],
                "country": "China",
                "alpha_two_code": "CN",
                "state-province": None
            }
        ]
        self.assertEqual(filtered_output, expected_output)

    def test_empty_source_data(self):
        filtered_output = country_filter([], "China")
        expected_output = []
        self.assertEqual(filtered_output, expected_output)

    def test_empty_country_scopes(self):
        filtered_output = country_filter(self.source_data, [])
        expected_output = self.source_data
        self.assertEqual(filtered_output, expected_output)


if __name__ == '__main__':
    unittest.main()
