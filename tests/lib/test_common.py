"""Tests for the shared utility functions"""


from unittest import TestCase

from maxer.lib.common import parse_color

class TestCommon(TestCase):
    def test_parses_color(self):
        self.assertEqual(parse_color('#fff'), (255, 255, 255))
        self.assertEqual(parse_color('#010101'), (1, 1, 1))
