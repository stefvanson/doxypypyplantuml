#!/usr/bin/env python3
"""Main module for developing/testing doxypypyplantuml.

"""
import argparse
import os
import subprocess
import sys

RUN_ALL_TESTS = "Run all"


def _run_unit_tests(args):
    command = ['python3', '-m', 'unittest']
    if args.unit in [RUN_ALL_TESTS, None]:
        # If only --unit specified or running just everything (i.e. unit == None)
        command += ['discover', './tests/']
    else:
        command += [args.unit]
    print(f"== Running unit tests ==\n> {' '.join(command)}\n")
    subprocess.run(command, check=False)


def _run_style_check():
    style_ignores = []
    command = ['pycodestyle',
               f'--ignore={",".join(style_ignores)}',
               '--max-line-length=90', 'src/doxypypyplantuml/', 'run.py']
    print(f"== Running style check ==\n> {' '.join(command)}\n")
    subprocess.run(command, check=False)


def _run_static_analysis():
    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join(sys.path)
    disabled_checks = []
    disabled_checks += ['missing-docstring']

    command = ['pylint', f'--disable={",".join(disabled_checks)}']
    command += ['src', 'run.py']
    print(f"== Running static analysis ==\n> {' '.join(command)}\n")
    subprocess.run(command, env=env, check=False)

    # Now run it on the tests with some relaxed checks
    disabled_checks += ['C0103']
    dirs_to_check = ['tests']
    command = ['pylint', f'--disable={",".join(disabled_checks)}']
    command += dirs_to_check
    print(f"== Running static analysis ==\n> {' '.join(command)}\n")
    subprocess.run(command, env=env, check=False)


def _create_argparser():
    description = ("Tool for executing diagnostic activities with a physical ECU, such as"
                   " reading and setting internal variables and flashing a new binary.")
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('--unit', action='store',
                           nargs='?', type=str, const=RUN_ALL_TESTS,
                           help="Runs the unit tests. Specify a value with the option "
                                "like tests.test_doxypypyplantuml to run specific tests.")
    argparser.add_argument('--style', action='store_true',
                           help="Runs the style checker.")
    argparser.add_argument('--static', action='store_true',
                           help="Runs the static analyzer.")
    return argparser


input_args = _create_argparser().parse_args()
print(input_args)
if input_args.unit:
    _run_unit_tests(input_args)
if input_args.style:
    _run_style_check()
if input_args.static:
    _run_static_analysis()
if not (input_args.unit or input_args.style or input_args.static):
    _run_unit_tests(input_args)
    _run_style_check()
    _run_static_analysis()
