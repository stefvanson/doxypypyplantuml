import os
import subprocess
import unittest.mock

import src.doxypypyplantuml.doxypypyplantuml as doxypypyplantuml


class DoxypypyPlantUmlTests(unittest.TestCase):
    def test_fake_input_file(self):
        # Execute the command of the proposed py_filter:
        # > doxypypy -a -c $1 | doxypypyplantuml $1
        input_filepath = os.path.join('tests', 'fake_input_file.py')
        output_filepath = os.path.join('tests', 'expected_output_file.py')
        command = ['doxypypy', '-a', '-c', input_filepath]
        # command += ['|', 'doxypypyplantuml', input_filepath]
        print(' '.join(command))
        completed_process = subprocess.run(command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           text=True)
        print(str(completed_process.stdout))
        ## @todo Implement the test:
        #        1. Open the fake_input_file.py
        #        2. Feed it through doxypypy
        #        3. Then feed it through doxypypyplantuml
        #        4. Verify the output agains expected_output_file.py
        # print(f"argv_mock = {argv_mock}")
        # Replace the mock by just a subprocess command?
        # argv_mock[1] = os.path.join('tests', 'fake_input_file.py')
        # doxypypyplantuml.main()
        self.assertTrue(False)
