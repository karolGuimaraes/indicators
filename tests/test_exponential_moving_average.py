import sys
sys.path.insert(1, '')
import unittest
import click
import pytest
from indicators.views import *
from click.testing import CliRunner


#class TestCase(unittest.TestCase):

# def test_hello_command():
#     print('oioio')
#     # python app.py --start=2021-01-01 --end=2022-01-31
#     runner = CliRunner()
#     result = runner.invoke(main, ['--start_date', '2021-01-01'])
#     assert "Flask" in result.output

def test_ema():
    current_price = 59.4
    last_ema = 60.4
    period = 3

    ema = exponential_moving_average(current_price, period, last_ema)

    assert ema == 59.9