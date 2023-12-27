import sys
sys.path.append('src')
from click.testing import CliRunner
from parquest.main import main

def test_main():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
