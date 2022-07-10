# DoxypypyPlantUML

> TLDR; if you are fed up with doxypypy screwing up your inlined PlantUML
> diagrams then this is probably what you are looking for.

PlantUML is great for incorporating UML diagrams in your software documentation.
If you have hybrid projects (containing for example both C and Python) you might
rely on Doxygen for generating some nice documentation. Typically, you can do
this by installing doxypypy, which transforms your Python docstrings into
Doxygen tagged documentation.

So far so good.

**Unfortunately, doxypypy performs some transformations when it
sees things like colons (it thinks it's an argument?); these are typically used
in docstrings for documenting for example function arguments. This can become
problematic when you are inlining PlantUML diagram code.** For an example refer
to "Bug Example" below.

One way to fix this is to fix it in doxypypy. Unfortunately the code is really
hard to understand and unmaintained.
This package, doxypypyplantuml, implements a simple and effective solution.

## How It Works

You simply provide it with the original file and the output
of doxypypy. Doxypypyplantuml will look for the `@startuml` and `@enduml` tags
(or \startuml and \enduml).
Everything in between these tags is part of the PlantUML Doxygen block.
It will replace everything in the doxypypy output between these tags by exactly
the same thing that was in the original file, only prefixing it with a `#` and
a correct amount of indentation.

## Installation

To install it simply use pip as usual, e.g.:

```sh
python3 -m pip install doxypypyplantuml
```

## Using it in your project

The steps are almost identical to the steps for
[setting up doxypypy](https://github.com/Feneric/doxypypy#invoking-doxypypy-from-doxygen).
Just follow the steps there, but there is one difference: You need to pipe the
output of doxypypy to doxypypyplantuml and provide the original input.

The py_filter file (for Unix-like operating systems) should therefore become:

```py
#!/bin/bash
doxypypy -a -c $1 | doxypypyplantuml $1
```

## Development notes

Before committing always first run `./run.py` and check the output.

Following the instructions on:
https://packaging.python.org/en/latest/tutorials/packaging-projects/

To build the package:

```bash
rm -r dist
python3 -m build
```

To upload the package to testpypi:

```bash
python3 -m twine upload --repository testpypi dist/*
```

pip install -i https://test.pypi.org/simple/ doxypypyplantuml==0.1.0

### Bug example

The following input, containing a PlantUML diagram in the class docstring, results in the
incorrect doxypypy output that's below it (it's invalid PlantUML syntax).

```py
class SomeStateMachine:
    """The state machine for bla bla.

    It comprehends the following state machine:

    @startuml
    State_A: On Entry / Transmit something
    State_A: During / Retry every second

    State_B: On Entry / Transmit GET_CCP_VERSION CRO
    State_B: During / Retry every second

    [*] -d-> State_A
    State_A -d-> State_B: connect()

    @enduml
    """
    def __init__(self, msg_handler: CcpMessageHandler):
        pass
```

```py
## @brief The state machine for bla bla.
#
#    It comprehends the following state machine:
#
#    @startuml
# 	State_A	On Entry / Transmit something
# 	State_A	During / Retry every second
#
# 	State_B	On Entry / Transmit GET_CCP_VERSION CRO
# 	State_B	During / Retry every second
#
#    [*] -d-> State_A
#    State_A -d-> State_B: connect()
#
#    @enduml
#
class SomeStateMachine:
    def __init__(self, msg_handler: CcpMessageHandler):
        pass
```
### To do list

- Add a changelog
- Look at classifiers of https://pypi.org/project/doxypypy/
- Upload for real
