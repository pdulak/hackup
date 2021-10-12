import os
import sys
import click

@click.command()
@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('destination_dir', type=click.Path(exists=True))
def perform_backup(source_dir, destination_dir):
    clone_directories(source_dir, destination_dir)


def clone_dir_if_not_present(dir_name, subdir_name, source_dir, destination_dir):
    this_src_dir = os.path.join(dir_name, subdir_name)
    this_dst_dir = this_src_dir.replace(source_dir, destination_dir)
    if not os.path.exists(this_dst_dir):
        os.makedirs(this_dst_dir)
        click.echo(f'Created: {this_dst_dir}')


def clone_directories(source_dir, destination_dir):
    click.echo(f'Clonning {source_dir} directory structure to {destination_dir}')
    for dir_name, dir_names, file_names in os.walk(source_dir):
        for subdir_name in dir_names:
            clone_dir_if_not_present(dir_name, subdir_name, source_dir, destination_dir)


if __name__ == '__main__':
    perform_backup()
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    #
    # clone_directories(source_dir, destination_dir)
