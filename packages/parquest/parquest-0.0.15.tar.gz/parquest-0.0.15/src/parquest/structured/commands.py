import click
from .convert.commands import convert
from .specs.commands import specs

@click.group()
def structured():
    """Collection of commands to operate Structured Zone"""
    pass

structured.add_command(convert)
structured.add_command(specs)