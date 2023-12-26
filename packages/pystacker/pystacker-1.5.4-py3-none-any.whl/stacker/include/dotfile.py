from __future__ import annotations

from pathlib import Path

from stacker.error import IncludeError
from stacker.include.stk_file_read import readtxt
from stacker.syntax.parser import remove_start_end_quotes
from stacker.lib.config import stacker_dotfile, script_extension_name


def execute_stacker_dotfile(filename: str | Path) -> "Stacker":
    """Import a stacker script and return the stacker object."""

    filename = remove_start_end_quotes(filename)
    if str(filename) != stacker_dotfile:
        raise IncludeError(f"File {filename} is not a stacker script.")

    # with open(filename, 'r') as file:
    # script_content = file.read()

    script_content = readtxt(filename)

    from stacker.stacker import Stacker

    stacker = Stacker()
    stacker.process_expression(script_content)
    return stacker
