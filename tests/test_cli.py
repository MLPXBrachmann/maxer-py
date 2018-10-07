"""Tests for the main maxer CLI module."""


from subprocess import PIPE, Popen as popen
from unittest import TestCase

from maxer import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['maxer', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)

        output = popen(['maxer', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['maxer', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION.encode())
