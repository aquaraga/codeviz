import os
import sys

def get_projects_to_scan(base):
    return list(filter(lambda x: os.path.isdir(os.path.join(base, x)), os.listdir(base)))


def get_base_dir():
    if 'BASE_DIR' not in os.environ:
        print('BASE_DIR environment variable must be set', file = sys.stderr)
        sys.exit(-1)
    base_dir = os.environ['BASE_DIR']
    if not os.path.isdir(base_dir):
        print('BASE_DIR environment variable must be a valid directory', file = sys.stderr)
        sys.exit(-2)
    return base_dir
