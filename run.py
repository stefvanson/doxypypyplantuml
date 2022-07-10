#!/usr/bin/env python3
"""Main module for developing/testing doxypypyplantuml.

"""
import argparse
import os
import shutil
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


def _build_and_upload(for_real=False):
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    command = ['python3', '-m', 'build']
    print(f"== Building package ==\n> {' '.join(command)}\n")
    subprocess.run(command, check=True)
    command = ['python3', '-m', 'twine', 'upload']
    if not for_real:
        command += ['--repository', 'testpypi', 'dist/*']
    else:
        command += ['dist/*']
    print(f"== Uploading package ==\n> {' '.join(command)}\n")
    subprocess.run(command, check=True)


def _create_argparser():
    description = ("Helper script for testing the doxypypyplantuml module.")
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('--upload', action='store_true',
                           help="Builds the package and uploads it to the *Test* Python "
                                "Package Index.")
    argparser.add_argument('--upload-release', action='store_true',
                           help="Builds the package and uploads it to the Python Package "
                                "Index.")
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
active_args = [True for arg in vars(input_args).values() if arg]
if input_args.upload:
    _build_and_upload(for_real=False)
if input_args.upload_release:
    _build_and_upload(for_real=True)
if input_args.unit:
    _run_unit_tests(input_args)
if input_args.style:
    _run_style_check()
if input_args.static:
    _run_static_analysis()
if not [True for arg in vars(input_args).values() if arg]:
    _run_unit_tests(input_args)
    _run_style_check()
    _run_static_analysis()
