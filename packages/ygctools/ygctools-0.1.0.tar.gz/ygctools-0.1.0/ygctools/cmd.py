# -*- coding:utf-8 -*-

from __future__ import print_function
import optparse
import sys
import os

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

__version__ = "0.1.0"

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-V' or sys.argv[1] == '--version':
            put_string(__version__)
            return
