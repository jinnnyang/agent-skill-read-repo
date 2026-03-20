#!/usr/bin/env python3
"""
Alias script for deepwiki_helper.py
"""
import os
import sys

# Add the script directory to sys.path to import deepwiki_helper
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from deepwiki_helper import main

if __name__ == "__main__":
    main()
