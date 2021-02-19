# disk-scan
A Python library to scan disks and clean it up.

## Install
```
$ make install
```

## For Developers
```
$ make developer

$ source .env/bin/activate
```
## Usage
```
$ python3 disk.py
Usage: disk.py [OPTIONS] COMMAND [ARGS]...

Commands:
  bigfiles    Find big files in DIR
  duplicate   Find duplicated files in DIR
  filtername  Scan and find files with names in DIR
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

**Find files by name**
```bash
# Scan and print to screen
python3 disk.py suffix ~/Downloads -n sunshine -n apple
# Scan and print to file
python3 disk.py suffix ~/Downloads -n juice --json=output.json
```
