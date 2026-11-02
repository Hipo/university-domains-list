import json
import os
import unittest


class BaseUniversityTest(unittest.TestCase):
    def setUp(self):
        """Load the JSON file into a variable"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(
            os.path.dirname(script_dir), "world_universities_and_domains.json"
        )
        with open(json_path, encoding="utf-8") as json_file:
            self.valid_json = json.load(json_file)
