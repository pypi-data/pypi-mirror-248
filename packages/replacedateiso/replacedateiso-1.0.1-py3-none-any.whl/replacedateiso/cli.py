"""CLI interface for replacedateiso project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
from pathlib import Path
import re, os

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m replacedateiso` and `$ replacedateiso `.

    This is your program's entry point.
    """

    for file in Path.cwd().iterdir():
        match = re.search('\d{2}.\d{2}.\d{4}', file.name)
        if match != None:
            dateparam = match.group().split(".")
            day = dateparam[0]
            month = dateparam[1]
            year = dateparam[2]
            newname = file.name.replace(match.group(), year + "-" + month + "-" + day)
            print("Found Date:" + file.name + " [ " + match.group() + " ] -> " + newname)
            os.rename(file, file.parent / newname)