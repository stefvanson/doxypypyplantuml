"""@file
This file contains tricky PlantUML input for doxypypy, which we use in
test_doxypypyplantuml.py to see if that fixes it correctly.

The tricky parts that are incorporated in this file are:
1. Both types of tags (starting with an @ and with a \) for both startuml and enduml.
2. A PlantUML block that contains colons and indentation, which is known to get screwed
   up by doxypypy.
3. PlantUML at different levels of indentation.

The same problematic PlantUML diagram can be found below. It's also put in the
AbcDef class docstring and the some_method docstring, with a small variation in
the names of the states (to detect if it is actually the right block).

Here it is for testing module docstrings and it's in @-style tags.

@startuml
State_A: On Entry / Transmit something
State_A: During / Retry every second

State_B: On Entry / Transmit GET_CCP_VERSION CRO
State_B: During / Retry every second

[*] -d-> State_A
State_A -d-> State_B: connect()
@enduml
"""

class AbcDef:
    """Some class for AbcDef

    Here is the problematic PlantUML diagram in a class docstring and it's in
    \-style tags.

    \startuml
    State_C: On Entry / Transmit something
    State_C: During / Retry every second

    State_D: On Entry / Transmit GET_CCP_VERSION CRO
    State_D: During / Retry every second

    [*] -d-> State_C
    State_C -d-> State_D: connect()

    \enduml
    """
    def __init__(self):
        pass

    def some_method(self, a):
        """This is the documentation for some_method, which has

        Here is the problematic PlantUML diagram in a method docstring and it's in
        mixed @- and \-style tags.

        @startuml
        State_E: On Entry / Transmit something
        State_E: During / Retry every second

        State_F: On Entry / Transmit GET_CCP_VERSION CRO
        State_F: During / Retry every second

        [*] -d-> State_E
        State_E -d-> State_F: connect()

        \enduml
        """
        return 1
