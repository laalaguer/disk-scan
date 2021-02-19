'''
Utils dealing with <Path>
These functions are stateless
'''

from typing import Iterable, Set, Dict, List, Callable
from pathlib import Path
import hashlib
import os


def is_mac_os_file(p: Path) -> bool:
    ''' Judge if a file is mac os hidden file '''
    if str(p.stem).startswith('._'): # Mac OS shadow files.
        return True
        
    if str(p.stem) == ".DS_Store": # Mac OS system files.
        return True
        
    return False


def pretty_str(p: Path, only_path=True) -> str:
    ''' Pretty string of the path '''
    buffer = [p]
    if not only_path:
        buffer.append(p.stat().st_size)
        buffer.append(p.suffix)
        buffer.append(p.stem)
        buffer.append(p.name)

    return '\n'.join(buffer)


def remove_file(p: Path, dry_run=True) -> None:
    ''' Remove a file, if file not found, won't fail '''
    if p.is_dir():
        raise Exception(f'{p} is not a file')

    if dry_run:
        print(f'Remove: {p}')
    else:
        try:
            p.unlink()
        except FileNotFoundError:
            pass


def remove_dir(p: Path, recursive=False, dry_run=True) -> None:
    '''
    Remove a directory.

    Note: If not recursive, and the directory isn't empty, will raise error.
    '''
    if not p.is_dir():
        raise Exception(f'{p} is not a directory')

    if ( not is_empty_dir(p) ) and ( not recursive ):
        raise Exception(f"{p} not empty, use recurisve=True to force remove.")
    
    # First, remove any content inside it.
    for x in p.iterdir():
        if x.is_dir():
            remove_dir(x, recursive, dry_run)
        else:
            remove_file(x, dry_run)

    # Then, remove the dir.
    if is_empty_dir(p):
        if dry_run:
            print(f'Remove: {p}')
        else:
            try:
                p.unlink()
            except FileNotFoundError:
                pass


def is_empty_dir(p: Path) -> bool:
    ''' Test if directory is empty '''
    if not p.is_dir():
        raise Exception(f'{p} is not a directory')

    return not any(p.iterdir())


def is_almost_empty_dir(p: Path) -> bool:
    '''
    If directory only contains os hidden files, then it is almost empty.
    '''
    if not p.is_dir():
        raise Exception(f'{p} is not a directory')
    
    if is_empty_dir(p):
        return True
    
    input = {x for x in p.iterdir()}
    output = exclude_os_files(input)

    return not (len(output) != 0)


def exclude_os_files(nodes: Set[Path]) -> Set[Path]:
    ''' Filter out mac os files from the set '''
    return {x for x in nodes if not is_mac_os_file(x)}


def filter_by_size(nodes: Set[Path], more_than:int=None, less_than:int=None) -> Set[Path]:
    ''' Filter nodes with size requirement
         
        more_than/less_than: how many bytes
    '''
    if more_than == None and less_than == None:
        raise Exception("Need one of: more_than/less_than")

    if more_than != None and less_than == None:
        return {x for x in nodes if x.stat().st_size > more_than}
    
    if more_than == None and less_than != None:
        return {x for x in nodes if x.stat().st_size < less_than}
    
    if more_than != None and less_than != None:
        if more_than >= less_than:
            raise Exception("more_than shall < less_than if both specified.")

        return {x for x in nodes if (x.stat().st_size < less_than) and (x.stat().st_size > more_than)}


def filter_by_suffixes(nodes: Set[Path], include: List[str]=None, exclude: List[str]=None) -> Set[Path]:
    ''' Filter nodes, include some, exclude some.
    
    Note: '.mp4' and '.MP4' are treated equally as '.mp4'
    '''
    if include == None and exclude == None:
        raise Exception("Need one of: include / exclude")
    
    if include != None and exclude != None:
        raise Exception("Can only fill in one of: include / exclude")

    if include:
        _include = [x.lower() for x in include]
        return {x for x in nodes if (not x.is_dir() and (x.suffix.lower() in _include))}

    if exclude:
        _exclude = [x.lower() for x in exclude]
        return {x for x in nodes if (not x.is_dir() and (x.suffix.lower() not in _exclude))}


def filter_by_name(nodes: Set[Path], include: List[str]=None, exclude: List[str]=None) -> Set[Path]:
    ''' Filter nodes, include some with partial name matching '''
    _include = []
    if include:
        _include = [str(x).lower() for x in include]
    
    _exclude = []
    if exclude:
        _exclude = [str(x).lower() for x in exclude]
    
    output = set()
    for x in nodes:
        should_add = False
        _x = str(x.stem).lower()
        for each in _include:
            if each in _x:
                should_add = True
                break
        
        for each in _exclude:
            if each in _x:
                should_add = False
                break
        if should_add:
            output.add(x)
    
    return output


def count_suffixes(nodes: Set[Path]) -> Dict:
    '''
    Go through the nodes, count the suffixes and their frequencies.

    Note: '.mp4' and '.MP4' are treated equally.

    Args:
        nodes (Set[Path]): A set of paths.

    Returns:
        Dict: {'.mp4': 345, '.avi': 456, ...}
    '''
    output = {}
    for x in nodes:
        if x.is_dir():
            continue
        current = str(x.suffix).lower()
        if current in output:
            output[current] += 1
        else:
            output[current] = 1
    
    return output


def scan(root: Path, call_back: Callable):
    '''
    Scan from root, get all dirs and files.

    When finished, call the 'call_back' with a set of paths.
    When processing, yeild total number (int) of scanned files.

    Args:
        root (Path): from path start to scan
        call_back (Callable): Accepts (Set[Path]) as only argument.

    Raises:
        Exception: If scanning path is not file nor dir.
    '''
    total_sum = 0
    all_nodes = set()
    unresolved = []
    unresolved.append(root.resolve())

    while len(unresolved) :
        current = unresolved.pop(0)
        total_sum += 1
        yield total_sum
        # File? Mark it.
        if current.is_file():
            all_nodes.add(current)
            continue
        
        # Directory? Go deeper.
        if current.is_dir():
            all_nodes.add(current)
            for x in current.iterdir():
                unresolved.append(x)
            continue
        
        continue
        # raise Exception(f"{current} is not file, nor dir")
    
    call_back(all_nodes)


def sort_nodes(nodes: Iterable[Path]) -> Iterable[Path]:
    ''' Sort a list of nodes.
    
    Shorter path: comes first.
    Shorter stem: comes first.

    Keep original if above rules doesn't apply.
    '''
    l = [len(str(node)) for node in nodes]
    if not (min(l) == max(l)):
        return sorted(nodes, key=lambda node: len(str(node)))  # path short first.
    
    s = [len(str(node.stem)) for node in nodes]
    if not (min(s) == max(s)):
        return sorted(nodes, key=lambda node: len(str(node.stem)))  # stem short first.

    return nodes


def rename_str(p: Path, old: str, new: str, dry_run=True) -> None:
    ''' Replace part of the name of the path. '''
    x = str(p)
    if old in x:
        y = x.replace(old, new)
        b = Path(y)
        if dry_run:
            print('Replace:')
            print('Old:', x)
            print('New:', y)
        else:
            p = p.rename(b)


def find_duplicates(nodes: Set[Path], call_back: Callable, ignore_stem: List[str]=None, ignore_suffix: List[str]=None, secure=False):
    '''
    Given a dict of nodes, find duplicated within it.
    Using MD5 hashing to determine if file are the same.

    During the process, it will yield current reading path.

    Args:
        call_back (Callable): Accepts (dict) as only argument.
        secure (bool): If secure, then md5 scan the whole file, otherwise only scan first 50MB.

    The call_back shall accept the only argument:
    {
        b'md5_hash': [Path, Path, ...],
        ...
    }
    '''
    _ignore_stem = None 
    if ignore_stem:
        _ignore_stem = [str(x).lower() for x in ignore_stem]
    
    _ignore_suffix = None
    if ignore_suffix:
        _ignore_suffix = [str(x).lower() for x in ignore_suffix]

    # Firstly, create a map:
    # size : [path, path, path]
    big = {}
    for node in nodes:
        skip_me = False
        if node.is_dir():
            skip_me = True
        if ignore_stem and node.stem.lower() in _ignore_stem:
            skip_me = True
        if ignore_suffix and node.suffix.lower() in _ignore_suffix:
            skip_me = True

        if skip_me:
            continue

        how_big = node.stat().st_size
        if big.get(how_big) == None:
            big[how_big] = [node]
        else:
            big[how_big].append(node)
    
    # Secondly, filter the map:
    # Keep only entries with size duplicates.
    filtered_big = {key:value for key, value in big.items() if len(value) > 1}
    
    # Thirdly, create a new map:
    # md5_hash: [path, path, path]
    md5_big = {}
    for size, items in filtered_big.items():
        for node in items:
            yield f'r{node}'
            m = hashlib.md5()
            b = None
            if secure:
                b = node.read_bytes()
            else:
                with open(node, 'rb') as f:
                    if node.stat().st_size > 60 * 1024 * 1024:  # Read first and last 30MB from file.
                        # Read first 30 MB
                        b = f.read(30 * 1024 * 1024)
                        # Jump to end 30 MB and read
                        f.seek(-30 * 1024 * 1024, os.SEEK_END)
                        b += f.read()
                    else:
                        b = node.read_bytes()
            m.update(b)
            k = m.digest()
            if md5_big.get(k) == None:
                md5_big[k] = [node]
            else:
                md5_big[k].append(node)
    
    # Last, now we have a exact duplicate table,
    # We trun only that md5 is duplicated.
    r_md5_big = {key: value for key, value in md5_big.items() if len(value) > 1}

    call_back(r_md5_big)
