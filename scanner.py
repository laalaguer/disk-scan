''' Command line interface to disk scan '''
from pathlib import Path
import click

@click.group()
def cli():
    pass

@click.command()
@click.argument('dir', type=str, required=True)
def duplicate(dir):
    ''' Search for duplicated files in a directory '''
    click.echo('Searching...')

@click.command()
@click.argument('dir', type=str, required=True)
@click.option('-s', '--size', type=int, default=1000, help='filter bigger than this size (mb)')
def bigfiles(dir, size):
    ''' Search for big files in a directory '''
    click.echo(f'Searching: {dir} with files larger than {size} mb')

cli.add_command(bigfiles)
cli.add_command(duplicate)


if __name__ == '__main__':
    cli()