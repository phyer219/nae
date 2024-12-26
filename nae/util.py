import os


def make_dir_exist(dest):
    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)