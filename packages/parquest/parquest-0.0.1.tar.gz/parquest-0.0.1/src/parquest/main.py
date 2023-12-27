import click

@click.command()
@click.version_option("0.0.1")
def main():
    click.echo("Version 0.0.1")

if __name__ == "__main__":
    main()
