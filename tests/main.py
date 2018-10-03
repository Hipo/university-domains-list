import json
import unittest
import requests

class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        with open("../world_universities_and_domains.json") as json_file:
            valid_json = json.load(json_file)
        for university in valid_json:
            university["name"]
            university["domains"]
            university["web_pages"]
            university["alpha_two_code"]
            university["state-province"]
            university["country"]

    def check_is_alive():
        """ check url then if url isn't alive, add to file """
        with open('../world_universities_and_domains.json') as json_raw:
            universities = json.load(json_raw)
        for university in universities[:]:
            try:
                for web_page in university["web_pages"]:
                    print(web_page)
                    requests.get(web_page, allow_redirects=False, timeout=10.0)
            except requests.exceptions.ConnectionError as exc:
                print('- Website doesn\'t exists: ', exc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
