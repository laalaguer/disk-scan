# disk-scan
A Python library to scan disks and clean it up.

## Install
```
$ make install
```

## For Developers
```
$ make develop
$ source .env/bin/activate
```

## Usage
```
$ ./disk.py
Usage: disk.py [OPTIONS] COMMAND [ARGS]...

Commands:
  bigfile    Find big files.
  byname     Find files with names.
  bysuffix   Filter out files with suffixes.
  duplicate  Find duplicated files.
  emptydir   Find empty directories.
  renamedir  Replace old name with new name, can be a partial replace.
```

## Examples

**Find duplicated files**
```bash
# Scan and print to screen
./disk.py duplicate ~/Downloads
# Scan and print to file
./disk.py duplicate ~/Downloads --json=output.json
```

**Find large files > 100MB**
```bash
# Scan and print to screen
./disk.py bigfile ~/Downloads --size=100
# Scan and print to file
./disk.py bigfile ~/Downloads --json=output.json
```

**Find files by suffix jpg or png**
```bash
# Scan and print to screen
./disk.py bysuffix ~/Downloads -s jpeg -s png
# Scan and print to file
./disk.py bysuffix ~/Downloads -s mp4 --json=output.json
```

**Find files by name**
```bash
# Scan and print to screen
./disk.py byname ~/Downloads -n sunshine -n apple
# Scan and print to file
./disk.py byname ~/Downloads -n juice --json=output.json
```

**Find empty directories**
```bash
./disk.py emptydir ~/Downloads
```

**Rename directory**
```bash
./disk.py renamedir ~/Downloads --old ninja --new gundam
```
