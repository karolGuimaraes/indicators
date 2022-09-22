import sys
sys.path.insert(1, '')
from indicators.views import main
from click.testing import CliRunner

def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert 0 == result.exit_code
