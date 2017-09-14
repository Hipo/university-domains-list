import json
import unittest
import requests

import validate_json

class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        validate_json.check_json_is_valid()

    def check_is_alive(url):
        """ check url then if url isn't alive, add to file """
        print(url)
        try:
            requests.get(url, allow_redirects=False, timeout=10.0)
        except requests.exceptions.ConnectionError as exc:
            print('- Website doesn\'t exists: ', exc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
