# Uses https://github.com/cgag/loc to find file-wise LOC for code-bases

import subprocess
import shlex
import os
import sys

def get_projects_to_scan(base):
    return list(filter(lambda x: os.path.isdir(os.path.join(base, x)), os.listdir(base)))

def filewise_loc_for_project(locPath, base, project):
    os.chdir(os.path.join(base, project))
    #TODO: Use temp file module
    f = open(r'metrics.txt','w')
    subprocess.check_call([locPath, 
        '--files', '--include', 'java$', '--exclude' ,'test'], stdout=f)
    f.close()
    with open('metrics.txt') as f:
        lines = f.read().splitlines()
    return list(map(lambda x: int(x.split()[-1]) ,lines[6:]))


def get_base_dir():
    if 'BASE_DIR' not in os.environ:
        print('BASE_DIR environment variable must be set', file = sys.stderr)
        sys.exit(-1)
    base_dir = os.environ['BASE_DIR']
    if not os.path.isdir(base_dir):
        print('BASE_DIR environment variable must be a valid directory', file = sys.stderr)
        sys.exit(-2)
    return base_dir


def main():
    base_dir = get_base_dir()
    wd = os.getcwd()
    os.chdir(base_dir)

    try:
        projects = get_projects_to_scan(base_dir)
        for project in projects:
            print(f'*** Printing loc_metrics for ${project}....')
            print(filewise_loc_for_project(f"{os.path.join(wd, 'loc')}",
              base_dir, project))
    except:
        _, value, _ = sys.exc_info()
        print('Error %s: %s' % (value.filename, value.strerror))
    finally:
        os.chdir(wd)


main()






