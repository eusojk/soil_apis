"""
This module makes a subprocess call to the fortran executable to produce a .SOL file
"""

import glob
import os
import subprocess
from pathlib import Path

path_to_exec = ''
output_dir = ''
arg_sample = ''


def dot_sol_api(script_dir):
    """

    :param script_dir: directory containing the actual script
    :return: path name of .SOL
    """
    global path_to_exec, arg_sample, output_dir
    # path_to_exec = os.path.abspath(script_dir)
    # output_dir = path_to_exec + '/outputs/'
    # path_to_exec += '/f90/dotSolAPI2.a'
    # path_to_exec = Path(path_to_exec)
    #
    # arg_sample = Path(sample_path)

    # check if both the exec and sample argument input exists
    if Path(path_to_exec).exists() and Path(arg_sample).exists():
        os.chdir(output_dir)
        args_run = [path_to_exec, arg_sample]
        subprocess.call(args_run)
        thsol = glob.glob(output_dir + '*.SOL')[0]
        return thsol


def soil_type_api(fracs):
    """

    :param fracs: list of two int - this value can be 0-100; Sand/Clay/Loam
    :return:
    """
    global path_to_exec, output_dir

    os.chdir(output_dir)

    args_run = str(path_to_exec) + ' ' + str(fracs[0]) + ' ' + str(fracs[1])

    # call the fortran exec and retrieve the value from the shell, then convert from bytes to str
    pipe = subprocess.Popen(args_run, shell=True, stdout=subprocess.PIPE).stdout
    output_shell = pipe.read().decode('UTF-8')

    # remove '\n' character from output
    soil_type = output_shell[:-1]
    return soil_type


def which_api(sample_path, script_dir, api_num, fracs=None):
    """
    Pick which api to use
    :param sample_path: sample file
    :param script_dir: directory of scripts
    :param api_num: 0 (TAW file) or code: 1 (SOL)
    :param fracs: this a list: [sand, clay]
    :return: string - value of soil type
    """
    global path_to_exec, arg_sample, output_dir

    outfile = ''

    if fracs is None:
        fracs = [50, 50]

    arg_sample = Path(sample_path)
    path_to_exec = os.path.abspath(script_dir)
    output_dir = path_to_exec + '/outputs/'
    path_to_exec += '/soilapis/'

    if api_num == 0:  # TAW

        path_to_exec += '/make_texture.a'
        path_to_exec = Path(path_to_exec)
        outfile = soil_type_api(fracs)

    elif api_num == 1:  # SOL
        path_to_exec += '/dotSolAPI2.a'
        path_to_exec = Path(path_to_exec)
        outfile = dot_sol_api(script_dir)

    return outfile


def main():
    pass


if __name__ == '__main__':
    main()
