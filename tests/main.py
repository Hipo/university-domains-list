import json
import validate_json
import unittest


class DomainsTests(unittest.TestCase):
    def test_json_is_valid(self):
        validate_json.check_json_is_valid()


if __name__ == '__main__':
    unittest.main(verbosity=2)
