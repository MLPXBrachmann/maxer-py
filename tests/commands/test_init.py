"""Tests for the init command"""

from unittest import TestCase

from maxer.lib.config import check_config

from maxer.commands.init import BASE_CONFIG

class TestInit(TestCase):
    def test_is_valid_config(self):
        self.assertTrue(check_config(BASE_CONFIG))
