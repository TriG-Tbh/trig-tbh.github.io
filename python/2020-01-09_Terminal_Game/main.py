#!/usr/bin/python3

import sys
import os


path = os.path.dirname(os.path.realpath(__file__)) + "/"

def basejoin(file):
    return os.path.join(path, file)


if "idlelib.run" in sys.modules:
    message = """why
in
the
hell
are you running scripts in idle
use a terminal
please
almost nothing in this program works if you're not using a terminal
idle will set you up for failure later in life
run this script only when you know how to run python scripts in a terminal"""
    raise ImportError(message)

