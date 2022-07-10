import os
import subprocess
import unittest.mock

import src.doxypypyplantuml.doxypypyplantuml as doxypypyplantuml


class DoxypypyPlantUmlTests(unittest.TestCase):
    def test_fake_input_file(self):
        # Execute the command of the proposed py_filter with fake_input_file.py:
        # > doxypypy -a -c $1 | doxypypyplantuml $1
        input_filepath = os.path.join('tests', 'test_doxypypyplantuml_resources',
                                      'fake_input_file.py')
        command = f"doxypypy -a -c {input_filepath}"
        command += f" | src/doxypypyplantuml/doxypypyplantuml.py {input_filepath}"
        stdout = subprocess.check_output(command, shell=True)
        stdout = stdout.decode("utf-8")

        # Verify the output agains expected_output_file.py
        output_filepath = os.path.join('tests', 'test_doxypypyplantuml_resources',
                                       'expected_output_file.py')
        with open(output_filepath, 'r') as output_file:
            line_nr = 0
            for output_line in stdout.split('\n'):
                expected_output_line = output_file.readline().rstrip()
                self.assertEqual(output_line, expected_output_line)
                line_nr += 1
