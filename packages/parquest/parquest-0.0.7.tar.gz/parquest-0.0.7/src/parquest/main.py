import click

@click.command()
@click.version_option("0.0.7")
def main():
    click.echo("Version 0.0.7")

if __name__ == "__main__":
    main()
