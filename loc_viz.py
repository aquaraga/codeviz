# Uses https://github.com/cgag/loc to find file-wise LOC for code-bases

import subprocess
import shlex
import os
import sys
import matplotlib.pyplot as plt
from common import get_base_dir, get_projects_to_scan

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

def main():
    base_dir = get_base_dir()
    wd = os.getcwd()
    os.chdir(base_dir)
    try:
        projects = get_projects_to_scan(base_dir)
        all_project_locs = [filewise_loc_for_project(f"{os.path.join(wd, 'loc')}",
              base_dir, x) for x in projects]
        _, ax = plt.subplots()
        ax.set_title('File-wise LOC distribution across projects')
        ax.boxplot(all_project_locs)
        ax.set_xticklabels(projects)
        plt.show() 
    except:
        _, value, _ = sys.exc_info()
        print('Error %s: %s' % (value.filename, value.strerror))
    finally:
        os.chdir(wd)

main()