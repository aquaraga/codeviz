# Uses https://github.com/terryyin/lizard to find function-wise complexity for code-bases

import subprocess
import shlex
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import get_base_dir, get_projects_to_scan

def comp_for_project(base, project):
    f = open(r'comp.csv','w')
    subprocess.check_call(['lizard', 
        os.path.join(base, project), "-x", "*Test*", "-l", "java", "--csv"], stdout=f)
    f.close()
    df = pd.read_csv('comp.csv')
    #print(df.head())
    return (df.iloc[:,1] > 5).sum()
def main():
    base_dir = get_base_dir()
    try:
        projects = get_projects_to_scan(base_dir)
        files_with_high_complexity = [comp_for_project(
              base_dir, x) for x in projects]
        print(files_with_high_complexity)
        
    except:
        _, value, _ = sys.exc_info()
        print('Error %s: %s' % (value.filename, value.strerror))

main()