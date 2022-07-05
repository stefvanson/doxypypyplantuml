"""
@file
@brief This file contains tricky PlantUML input for doxypypy, which we use in
       test_doxypypyplantuml.py to see if that fixes it correctly.
@details

The tricky parts that are incorporated in this file are:
1. Both types of tags (starting with an @ and with a \) for both startuml and enduml.
2. A PlantUML block that contains colons and indentation, which is known to get screwed
   up by doxypypy.
3. PlantUML at different levels of indentation.
"""

class AbcDef:
    ## @brief Hi
    def __init__(self) -> None:
        pass

    def Hi(self, a):
        return 1
