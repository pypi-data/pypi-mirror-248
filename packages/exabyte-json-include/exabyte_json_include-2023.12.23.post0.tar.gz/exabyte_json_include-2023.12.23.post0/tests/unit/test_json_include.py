import unittest
from textwrap import dedent

import json_include

class TestJsonIncludeUnit(unittest.TestCase):
    def test_build_json_simple(self):
        json = json_include.build_json('./tests/unit/fixtures', 'simple_example.json')
        intended_result = dedent("""
        {
            "one": "fish",
            "two": "phish",
            "red": "fishe",
            "blue": "phishe"
        }
        """).strip()
        self.assertEqual(json, intended_result)

    def test_build_json_with_include(self):
        json = json_include.build_json('./tests/unit/fixtures', 'import_example.json')
        intended_result = dedent("""
        {
            "one": "fish",
            "two": "phish",
            "red": "fishe",
            "blue": "phishe",
            "an_include": {
                "peter": "piper"
            }
        }
        """).strip()
        self.assertEqual(json, intended_result)

