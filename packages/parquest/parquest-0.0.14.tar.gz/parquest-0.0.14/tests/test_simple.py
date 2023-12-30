import sys
sys.path.append('src')
from click.testing import CliRunner
from parquest.main import cli

def test_main():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
