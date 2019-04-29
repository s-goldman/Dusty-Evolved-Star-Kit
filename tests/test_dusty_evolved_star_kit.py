#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dusty_evolved_star_kit` package."""


import unittest
from click.testing import CliRunner

from dusty_evolved_star_kit import dusty_evolved_star_kit
from dusty_evolved_star_kit import cli


class TestDusty_evolved_star_kit(unittest.TestCase):
    """Tests for `dusty_evolved_star_kit` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'dusty_evolved_star_kit.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
