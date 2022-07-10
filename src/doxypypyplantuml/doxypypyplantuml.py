#!/usr/bin/env python3
"""Package contain the doxypyplantuml implementation. More information can be found in the
project's README.md.
"""
import argparse
import sys
from typing import List


class PlantUmlBlock:
    """Class for a block of lines that together make up a PlantUML diagram, i.e. the lines
    between the start and the end tag including the tags.
    """
    def __init__(self, lines):
        self._lines = self._get_lines_with_normalized_indentation(lines)

    def _get_lines_with_normalized_indentation(self, lines):
        startuml_line = lines[0]
        indent = self._get_index_of_start_tag(startuml_line)
        output_lines = []
        for line in lines:
            if line[indent:]:
                output_lines.append(line[indent:])
            else:
                output_lines.append("\n")
        return output_lines

    def _get_index_of_start_tag(self, line):
        # Tag can start with an @ or an \ in Doxygen
        return max(line.find('@'), line.find('\\'))

    def output_in_doxypypy_style(self, doxypypy_line):
        """Outputs the PlantUmlBlock in the same style as doxypypy, so starting with the
        right indentation and starting with a #, to stdout.

        Args:
            doxypypy_line: The original first line of the doxypypy output, which is used
                to detect the indentation.
        """
        indentation = self._detect_indentation(doxypypy_line)
        for line in self._lines:
            print(' ' * indentation + '#' + line.rstrip())

    def _detect_indentation(self, line):
        return line.find('#')

    def __str__(self):
        block = "#### BLOCK_START ####\n"
        for line in self._lines:
            block.join(line)
        block += "#### BLOCK_END ####"
        return block


class PlantUmlBlockFinder:
    """Class for locating the PlantUML code blocks in a file.
    """
    def __init__(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as file:
            self._lines = file.readlines()
        self._blocks = self.parse_plantuml_blocks()

    def parse_plantuml_blocks(self) -> List[PlantUmlBlock]:
        """Parses the file for PlantUML code blocks

        Returns:
            List[PlantUmlBlock]: The list of UML blocks that were found in the file.
        """
        blocks = []
        for line_number, line in enumerate(self._lines):
            if self.line_contains_startuml_tag(line):
                start = line_number
            elif self.line_contains_enduml_tag(line):
                end = line_number
                blocks.append(self._create_block(start, end))
        return blocks

    @staticmethod
    def line_contains_startuml_tag(line: str) -> bool:
        """Checks whether the line contains a valid Doxygen startuml tag.

        Args:
            line (str): The line in which to check for the tag.

        Returns:
            bool: True if it contains a tag, False otherwise.
        """
        return ('@startuml' in line) or (r'\startuml' in line)

    @staticmethod
    def line_contains_enduml_tag(line: str) -> bool:
        """Checks whether the line contains a valid Doxygen enduml tag.

        Args:
            line (str): The line in which to check for the tag.

        Returns:
            bool: True if it contains a tag, False otherwise.
        """
        return ('@enduml' in line) or (r'\enduml' in line)

    def _create_block(self, start, end) -> PlantUmlBlock:
        """Creates a block, containing all lines of that were between a start- and end tag
        including the lines with the tags.

        Returns:
            PlantUmlBlock: The created block.
        """
        if not start:
            raise Exception("@enduml encountered with unmatched @startuml")
        plantuml_lines = self._lines[start:end + 1]
        return PlantUmlBlock(plantuml_lines)

    def get_plantuml_block(self, index: int) -> PlantUmlBlock:
        """Gets the n-th plantuml code block in the documentation.

        Args:
            index (int): The n-th occurrence in the file where we start counting at 0.
        """
        return self._blocks[index]


class DoxypypyPlantUml:
    def __init__(self, original_input_file: str):
        self._block_finder = PlantUmlBlockFinder(original_input_file)

    def process_input(self):
        """Read input from stdin and process it by putting the original PlantUML blocks
        back in once they are encountered.

        It works as follows. It normally simply prints stdin to stdout.
        Whenever we come across a startuml tag we simply stop printing the lines until
        we encounter an enduml tag. Then we inject back the original uml block content
        with correct indentation.
        """
        skip_uml_line = False
        uml_block_index = 0
        for current_line in sys.stdin:
            current_line = current_line.rstrip()
            if PlantUmlBlockFinder.line_contains_startuml_tag(current_line):
                skip_uml_line = True
            elif PlantUmlBlockFinder.line_contains_enduml_tag(current_line):
                current_block = self._block_finder.get_plantuml_block(uml_block_index)
                current_block.output_in_doxypypy_style(current_line)
                uml_block_index += 1
                skip_uml_line = False
            elif not skip_uml_line:
                print(current_line)


if __name__ == "__main__":
    description = ("Tool for correcting Doxygen PlantUML code blocks in doxypypy output. "
                   "This tool is intended to be used in tandem with doxypypy. "
                   "Please follow the usage instructions of doxypypy and update your "
                   "py_filter file to contain `doxypypy -a -c $1 | doxypypyplantuml $1`.")
    argparser = argparse.ArgumentParser(prog="doxypypylantuml",
                                        description=description)
    argparser.add_argument("original_file", help="The original input file, from which the"
                           " PlantUML blocks are taken for the output.")
    args = argparser.parse_args()
    program = DoxypypyPlantUml(args.original_file)
    program.process_input()