import sys
sys.path.insert(1, '')
from indicators.views import main
from click.testing import CliRunner

def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert 0 == result.exit_code

def test_cli_invalid_date():
    runner = CliRunner()
    result = runner.invoke(main, ['--start_date', '2021-05-32'])

    assert 1 == result.exit_code
    assert 'Incorrect data format.' in result.output

def test_cli_no_data():
    runner = CliRunner()
    result = runner.invoke(main, ['--start_date', '2030-05-31'])

    assert 1 == result.exit_code
    assert 'No data.' in result.output