import click
from .raw.commands import raw
from .structured.commands import structured

@click.group()
def cli():
    pass

cli.add_command(raw)
cli.add_command(structured)