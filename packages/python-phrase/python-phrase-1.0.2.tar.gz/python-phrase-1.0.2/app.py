#!/usr/bin/env python

import click

@click.group()
def cli():
    pass

@cli.command()
def quote():
    """Prints the phrase 'Hello there, World!'"""
    click.echo("Hello there, World!")

if __name__ == '__main__':
    cli()
