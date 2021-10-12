Hackup backup script
====================

Purpose:
--------

Create packages of the files from source directory (divided into subdirectories)
in the destination directory. Such a set of packed directories can be sent to the backup server using rsync.

The script is checking for changes in the source directories (one by one, recursive)
and generates only missing packages or packages of directories that changed. This means that only packages that changed
between the last backup and current backup will be transferred. 

