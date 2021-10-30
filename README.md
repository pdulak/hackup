Hackup backup script
====================

Usage:
------

hackup.py [OPTIONS] /source/dir/ /destination/dir/

`/source/dir` - the source directory of to be backed up

`/destination/dir` - the directory to create archive into

`--password MyPassword` - create packages using password of 'MyPassword' (optional)

Purpose:
--------

Create packages of the files from source directory (divided into subdirectories)
in the destination directory. Such a set of packed directories can be sent to the backup server using rsync.

The script is checking for changes in the source directories (one by one, recursive)
and generates only missing packages or packages of directories that changed. This means that only packages that changed
between the last backup and current backup will be transferred.

Installation:
-------------

Clone the repository:

```
git clone git@github.com:pdulak/hackup.git
```

Create virtual environment:

```
cd hackup
virtualenv venv
```

Install dependencies:

```
./venv/bin/pip install -r requirements.txt
```

Enjoy:

```
./venv/bin/python hackup.py [OPTIONS] /source/dir/ /destination/dir/
```