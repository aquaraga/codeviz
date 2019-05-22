# Uses https://github.com/kucherenko/jscpd to find code duplication

import subprocess
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common import get_base_dir, get_projects_to_scan

token_range_for_cpds = np.arange(5, 20, 3)

def cpd_for_project_with_min_lines(base, project, lines):
    subprocess.check_call(['jscpd', '--format', 'java', '--mintokens', str(lines * 10),
        'min-lines', str(lines), '--ignore', '**/*Test.java', '-r', 'json', 
        os.path.join(base, project)])
    
    with open('report/jscpd-report.json') as json_file:
        data = json.load(json_file)
        os.remove(json_file.name)
        return float(data['statistics']['total']['percentage'])

def cpd_for_project(base, project):
    return list(map(
        lambda lines: cpd_for_project_with_min_lines(base, project, lines),
        token_range_for_cpds))

def line_plot(df):
    plt.style.use('seaborn-darkgrid')
    my_dpi = 96
    plt.figure(figsize = (480/my_dpi, 480/my_dpi), dpi = my_dpi)
    # multiple line plots
    for column in df.drop('x', axis = 1):
        plt.plot(df['x'], df[column], marker = '', linewidth = 1, alpha = 0.4)
    plt.xticks(np.arange(5, 20, 3))
    num = 0
    for i in df.values[0][1:]:
        num += 1
        name = list(df)[num]
        plt.text(5, i, name, horizontalalignment = 'left', size = 'small')

    plt.title("Code duplication in projects", fontsize = 12, fontweight = 0)
    plt.xlabel("Minimum lines to consider for duplication")
    plt.ylabel("Duplication (%)")
    plt.show()

def main():
    base_dir = get_base_dir()
    try:
        projects = get_projects_to_scan(base_dir)
        all_project_cpds = [(x, cpd_for_project(base_dir, x)) for x in projects]
        df = pd.DataFrame({'x': token_range_for_cpds})
        for project, cpds in all_project_cpds:
            df[project] = cpds
        line_plot(df)
        print(df)
    except:
        _, value, _ = sys.exc_info()
        print('Error %s: %s' % (value.filename, value.strerror))
    
main()