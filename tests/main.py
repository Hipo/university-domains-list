import json
import unittest
import requests

import validate_json

class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        validate_json.check_json_is_valid()

    def check_is_alive():
        """ check url then if url isn't alive, add to file """
        with open('../world_universities_and_domains.json') as json_raw:
            universities = json.load(json_raw)
        for university in universities[:]:
            try:
                # TODO: Test with multiple domains
                requests.get(university['web_pages'][0], allow_redirects=False, timeout=10.0)
            except requests.exceptions.ConnectionError as exc:
                print('- Website doesn\'t exists: ', exc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
