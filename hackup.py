import os
import click
import json
import hashlib

#
# TODO: Add an option to remove directories if removed on source side
# TODO: Ability to provide password to protect packages
#

@click.command()
@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('destination_dir', type=click.Path(exists=True))
def perform_backup(source_dir, destination_dir):
    """
    Performs backup of source directory in destination directory by creating packages of files
    :param source_dir:
    :param destination_dir:
    :return:
    """
    clone_directories(source_dir, destination_dir)
    generate_packages(source_dir, destination_dir)


def clone_dir_if_not_present(dir_name, subdir_name, source_dir, destination_dir):
    """
    Clone particular directory from source_dir to destination_dir if not present
    """
    this_src_dir = os.path.join(dir_name, subdir_name)
    this_dst_dir = this_src_dir.replace(source_dir, destination_dir)
    if not os.path.exists(this_dst_dir):
        os.makedirs(this_dst_dir)
        click.echo(f'Created: {this_dst_dir}')


def clone_directories(source_dir, destination_dir):
    """
    Creates clone of directory structure of source directory in destination directory
    """
    click.echo(f'Clonning {source_dir} directory structure to {destination_dir}')
    for dir_name, dir_names, file_names in os.walk(source_dir):
        for subdir_name in dir_names:
            clone_dir_if_not_present(dir_name, subdir_name, source_dir, destination_dir)


def generate_files_hash(file_names, dir_name):
    """
    Generates hash of files in directory using their names and parameters such as size, creation and modification date
    :param file_names: list of file names
    :param dir_name: directory where the files are located
    :return: hash of the file names and parameters
    """
    files_data = []
    for file_name in file_names:
        files_data.append([file_name, os.stat(os.path.join(dir_name, file_name))])
    return hashlib.md5(json.dumps(files_data, sort_keys=True).encode('utf-8')).hexdigest()


def generate_packages(source_dir, destination_dir):
    """
    Generates packages of files located in particular source directory if files hash changed
    :param source_dir:
    :param destination_dir:
    :return:
    """
    click.echo(f'Generating packages of files from {source_dir} subdirectories in {destination_dir}')
    for dir_name, dir_names, file_names in os.walk(source_dir):
        click.echo(f'Directory of: {dir_name} contains {len(file_names)} files')
        if len(file_names) > 0:
            files_hash = generate_files_hash(file_names, dir_name)
            click.echo(f'Result of listing is hash of {files_hash}')
            this_dst_dir = dir_name.replace(source_dir, destination_dir)
            click.echo(f'Checking files in destination directory of {this_dst_dir}')
            # TODO: check if package of this hash exists and create one
            # TODO: remove packages of different hash from the same directory


if __name__ == '__main__':
    perform_backup()
