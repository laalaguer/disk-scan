# disk-scan
A Python library to scan disks and clean it up.

## Install
```
make install
```

## Usage
```
$ python3 disk.py
Usage: disk.py [OPTIONS] COMMAND [ARGS]...

Commands:
  bigfiles    Find big files in DIR
  duplicate   Find duplicated files in DIR
  suffix      Scan the DIR and filter out files with certain suffixes.
```

## Examples

**Find duplicated files**
```bash
# Scan and print to screen
python3 disk.py duplicate ~/Downloads
# Scan and print to file
python3 disk.py duplicate ~/Downloads --json=output.json
```

**Find large files > 100MB**
```bash
# Scan and print to screen
python3 disk.py bigfiles ~/Downloads --size=100
# Scan and print to file
python3 disk.py bigfiles ~/Downloads --json=output.json
```

**Find files by suffix jpg or png**
```bash
# Scan and print to screen
python3 disk.py suffix ~/Downloads -s jpeg -s png
# Scan and print to file
python3 disk.py suffix ~/Downloads -s mp4 --json=output.json
```