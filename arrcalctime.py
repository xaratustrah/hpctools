#!/usr/bin/env python
"""
calculate start and end of slurm calculation arrays

xaratustrah dec-2022
"""

import subprocess
import sys
import numpy as np


def run_cmd(cmd_string):
    try:
        p = subprocess.Popen(cmd_string.split(),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = p.wait()
        out, err = p.communicate()
    except FileNotFoundError:
        out = b''
        err = b''
        ok = True

    return ok, out, err


if not len(sys.argv) == 2:
    print('Please enter the main part of the job ID.')
    sys.exit()

proc_number = sys.argv[1]

ok, out, err = run_cmd(f'sacct -j {proc_number}* --format=submit')
start = np.array(out.split()[2:], dtype='datetime64').min()

ok, out, err = run_cmd(f'sacct -j {proc_number}* --format=end')
end = np.array(out.split()[2:], dtype='datetime64').max()

print('Calculation time of job', sys.argv[1], 'took', end-start)
