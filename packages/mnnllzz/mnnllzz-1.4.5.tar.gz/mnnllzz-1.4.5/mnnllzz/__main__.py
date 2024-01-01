#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import glob
import json
import re

from .mnnllzz import typeset_tests

texfiles = glob.glob("*.tex")

if (len(texfiles) < 1):
    sys.exit("TeX file not found in current directory.")
elif (len(texfiles) > 1):
    sys.exit("More than one TeX file found in current directory.")
else:
    print("\n  >> mnnllzz <<\n")

files = open(texfiles[0],"r").read().split("MNNLLZZ")

template_text = files[0]
try:
    # Parse the JSON code in the source file.
    params = json.loads(files[1])
except ValueError as jerr:
    # Get the line with the error.
    errline = files[1].split("\n")[jerr.lineno-1]
    # Print info on the error.
    print("\033[1;31m\nFormula parsing error: %s.\033[0;0m\n" % jerr)
    print(errline.strip())
    sys.exit("Stop.")

typeset_tests(params, template_text)
