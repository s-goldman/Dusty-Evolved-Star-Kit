#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dusty_evolved_star_kit` package."""


import unittest
from click.testing import CliRunner

import desk
import os
import time
from desk import sed_fit, config
# from dusty_evolved_star_kit import cli


class TestDusty_evolved_star_kit(unittest.TestCase):
    """Tests for `dusty_evolved_star_kit` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        config.output["create_figure"] = 'No'
        sed_fit.fit()
        assert os.path.getmtime('fitting_results.csv') - time.time() <60
        assert os.stat('fitting_results.csv').st_size == 203
    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(sed_fit.fit())
    #     assert result.exit_code == 0
    #     assert 'Time:' in result.output
        
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
