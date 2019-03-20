#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)

from sop.sop import cli

if __name__ == "__main__":
    cli()
