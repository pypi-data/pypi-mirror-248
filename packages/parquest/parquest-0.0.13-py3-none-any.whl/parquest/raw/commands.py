import click
from .extract.commands import extract

@click.group()
def raw():
    """Collection of commands to operate Raw Zone"""
    pass

raw.add_command(extract)