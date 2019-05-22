# Uses https://github.com/cgag/loc to find file-wise LOC for code-bases

import subprocess
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common import get_base_dir, get_projects_to_scan

def cpd_for_project_with_min_lines(base, project, lines):
    subprocess.check_call(['jscpd', '--format', 'java', '--mintokens', str(lines * 10),
        'min-lines', str(lines), '--ignore', '**/*Test.java', '-r', 'json', 
        os.path.join(base, project)])
    
    with open('report/jscpd-report.json') as json_file:
        data = json.load(json_file)
        print('Duplication percentage is ', data['statistics']['total']['percentage'])
        return data['statistics']['total']['percentage']

def cpd_for_project(base, project):
    return list(map(
        lambda lines: cpd_for_project_with_min_lines(base, project, lines),
        np.arange(5, 20, 3)))


def main():
    base_dir = get_base_dir()
    try:
        projects = get_projects_to_scan(base_dir)
        all_project_cpds = [cpd_for_project(base_dir, x) for x in projects]
        print(all_project_cpds)
    except:
        _, value, _ = sys.exc_info()
        print('Error %s: %s' % (value.filename, value.strerror))
    
main()