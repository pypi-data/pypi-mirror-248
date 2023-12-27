#!/usr/bin/env python

import click

@click.group()
def cli():
    pass

@cli.command()
def quote():
    """Imprime a frase 'Thuta brincando de choco é?'."""
    click.echo("Thuta brincando de choco é?")

if __name__ == '__main__':
    cli()
