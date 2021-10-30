import hashlib
import json
import os

import click
import pyzipper


#
# TODO: Add an option to remove directories if removed on source side
# TODO: Check how to distribute such a script? How to do it so it is easy to execute?
#

@click.command()
@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('destination_dir', type=click.Path(exists=True))
@click.option('--password', default='', help='Provide password to create password-protected packages')
def perform_backup(source_dir, destination_dir, password):
    """
    Performs backup of source directory in destination directory by creating packages of files
    :param source_dir: Source directory
    :param destination_dir: Destination directory
    :param password: Password to create password-protected ZIP package
    :return:
    """
    clone_directories(source_dir, destination_dir)
    generate_packages(source_dir, destination_dir, password)


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


def pack_files(package_name, dst_dir, src_dir, src_file_names, password):
    """
    Creates package of source files in destination directory
    :param package_name: the name of ZIP file
    :param dst_dir: destination dir where the package will be placed
    :param src_dir: source dir of files to be compressed
    :param src_file_names: list of files to be compressed
    :param password: password to create password-protected ZIP package
    """
    click.echo(f'Creating package: {package_name}')

    if password == '':
        zf = pyzipper.ZipFile(os.path.join(dst_dir, package_name), 'w', compression=pyzipper.ZIP_LZMA)
    else:
        zf = pyzipper.AESZipFile(os.path.join(dst_dir, package_name), 'w', compression=pyzipper.ZIP_LZMA,
                                 encryption=pyzipper.WZ_AES)
        zf.setpassword(password.encode('utf-8'))

    for file_name in src_file_names:
        zf.write(os.path.join(src_dir, file_name), file_name)

    zf.close()


def remove_unwanted_files(package_name, dst_dir, dir_files):
    """
    Removes files different from the package name from the destination dir
    :param package_name: the package name to leave in place (do not remove)
    :param dst_dir: destination directory
    :param dir_files: list of files in destination directory
    """
    if package_name in dir_files:
        dir_files.remove(package_name)
    for file in dir_files:
        click.echo(f'Removing unwanted {file}')
        os.remove(os.path.join(dst_dir, file))


def create_package_if_missing_remove_unwanted(files_hash, dst_dir, src_dir, src_file_names, password):
    """
    Check if package exists, creates one if missing, removes old packages
    :param files_hash: the hash of the source directory
    :param dst_dir: destination dir where the package should be place
    :param src_dir: source dir of files to be compressed
    :param src_file_names: list of files to be compressed
    :param password: password to create password-protected ZIP package
    """
    package_name = (files_hash + '.zip' if password == '' else files_hash + '_e.zip')
    dir_files = [f for f in os.listdir(dst_dir) if os.path.isfile(os.path.join(dst_dir, f))]
    if package_name in dir_files:
        click.echo(f'Package {package_name} exists, no need to create')
    else:
        pack_files(package_name, dst_dir, src_dir, src_file_names, password)

    remove_unwanted_files(package_name, dst_dir, dir_files)


def generate_packages(source_dir, destination_dir, password):
    """
    Generates packages of files located in particular source directory if files hash changed
    :param source_dir:
    :param destination_dir:
    :param password: password to create password-protected ZIP package
    """
    click.echo(f'Generating packages of files from {source_dir} subdirectories in {destination_dir}')
    for dir_name, dir_names, file_names in os.walk(source_dir):
        click.echo(f'\nDirectory of: {dir_name} contains {len(file_names)} files')
        if len(file_names) > 0:
            files_hash = generate_files_hash(file_names, dir_name)
            this_dst_dir = dir_name.replace(source_dir, destination_dir)
            create_package_if_missing_remove_unwanted(files_hash, this_dst_dir, dir_name, file_names, password)


if __name__ == '__main__':
    perform_backup()
