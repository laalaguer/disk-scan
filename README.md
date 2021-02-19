# disk-scan
A Python library to scan disks and clean it up.

## Install
```
make install
```

## Usage
```
$ python3 disk.py --help
Usage: disk.py [OPTIONS] COMMAND [ARGS]...

Commands:
  bigfiles    Find big files in DIR
  cleanempty  Scan the DIR, clean up empty directories.
  duplicate   Find duplicated files in DIR
  suffix      Scan the DIR and filter out files with certain suffixes.
```

## Examples

**Find duplicate files**
```
python3 disk.py duplicate ~/Downloads --json=result.json
```

**Find large files > 100MB**
```
python3 disk.py bigfiles ~/Downloads --json=result.json
```