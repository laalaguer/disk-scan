''' Command line interface to disk scan '''
from typing import Set
from pathlib import Path
from disk_scan import utils
import click
import json


class Cache:
    def __init__(self):
        self.a = None
    
    def get(self):
        return self.a

    def populate(self, a):
        self.a = a


def progress(p: Path, show_progress=True) -> Cache:
    cache = Cache()
    for counter in utils.scan(p, cache.populate):
        if show_progress:
            print(f'\rSearching: {str(p)} {counter}', end='')
    print()
    return cache


def d_progress(nodes: Set[Path], show_progress=True) -> Cache:
    cache = Cache()
    for current in utils.find_duplicates(nodes, cache.populate):
        if show_progress:
            show = str(current)
            show = show if len(show) < 79 else show[:75] + '...'
            print(f'\rReading: {show}', end='')
    print('')
    return cache


@click.group()
def cli():
    pass


@click.command()
@click.argument('dir', type=click.Path(exists=True, dir_okay=True, resolve_path=True), required=True)
@click.option('--json', 'json_', type=str, default=None, help='File name to save the result in json')
@click.option('--include-sys', is_flag=True, default=False, help='Include system files in scan.')
def duplicate(dir, json_, include_sys):
    '''
    Find duplicated files in DIR
    '''
    p = Path(str(dir))
    cache = progress(p)
    nodes = cache.get()
    if not include_sys:
        nodes = utils.exclude_os_files(nodes)
    
    cache = d_progress(nodes)
    result = cache.get()

    if not json_:
        for md5_hash, paths in result.items():
            click.echo(md5_hash.hex())
            for x in paths:
                click.echo(str(x))
            click.echo('-' * 32)
    else:
        with open(json_, 'w') as f:
            r = {md5_hash.hex(): [str(x) for x in paths] for md5_hash, paths in result.items()}
            json.dump(r, f, indent=2)


@click.command()
@click.argument('dir', type=click.Path(exists=True, dir_okay=True, resolve_path=True), required=True)
@click.option('-s', '--size', type=int, required=True, prompt="Bigger than () MB?", help='Filter bigger than ? MB.')
@click.option('--json', 'json_', type=str, default=None, help='File name to save the result in json')
def bigfiles(dir, size, json_):
    '''
    Find big files in DIR
    '''
    click.echo(f'> {size} mb.')
    p = Path(str(dir))
    cache = progress(p)
    nodes = cache.get()

    result = utils.filter_by_size(nodes, more_than=size * (1024 * 1024))
    if not json_:
        for each in result:
            click.echo(each)
    else:
        with open(json_, 'w') as f:
            r = {'paths': [str(x) for x in result]}
            json.dump(r, f, indent=2)


@click.command()
@click.argument('dir', type=click.Path(exists=True, dir_okay=True, resolve_path=True), required=True)
@click.option('-s', '--suffix', multiple=True, default=[], required=True, help="eg. mp4, png, jpg")
@click.option('--json', 'json_', type=str, default=None, help='File name to save the result in json')
def suffix(dir, suffix, json_):
    '''
    Scan the DIR and filter out files with certain suffixes.
    
    You can supply multiple suffixes with multiple '-s' switch.
    '''
    _suffixes = ['.'+str(x).lower() for x in suffix if len(x.strip()) > 0]
    if len(_suffixes) == 0:
        click.echo('The suffixes provided cannot be white spaces!')
        return

    p = Path(str(dir))
    cache = progress(p)
    nodes = cache.get()

    result = utils.filter_by_suffixes(nodes, _suffixes)
    if not json_:
        for each in result:
            click.echo(each)
    else:
        with open(json_, 'w') as f:
            r = {'paths': [str(x) for x in result]}
            json.dump(r, f, indent=2)


# @click.command()
# @click.argument('dir', type=click.Path(exists=True, dir_okay=True, resolve_path=True), required=True)
# @click.option('--dryrun', is_flag=True, help='No actions, a dry run.')
# def rename(dir, dryrun):
#     '''
#     Replace old name with new name in a DIR, can be a partial replace
#     '''
#     click.echo(f'{dryrun}')


# @click.command()
# @click.argument('dir', type=click.Path(exists=True, dir_okay=True, resolve_path=True), required=True)
# @click.option('--dryrun', is_flag=True, help='No actions, a dry run.')
# def cleanempty(dir, dryrun):
#     '''
#     Scan the DIR, clean up empty directories.
#     '''
#     p = Path(str(dir))
#     cache = progress(p)
#     nodes = cache.get()


cli.add_command(bigfiles)
cli.add_command(duplicate)
cli.add_command(suffix)
# cli.add_command(rename)
# cli.add_command(cleanempty)


if __name__ == '__main__':
    cli()
