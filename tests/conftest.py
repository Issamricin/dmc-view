import os
import sys

# Get the directory of the current file (conftest.py)
current_dir = os.path.dirname(__file__)

# Construct the path to the src directory
src_path = os.path.abspath(os.path.join(current_dir, '../src/dmcview'))

# Insert it into sys.path
sys.path.insert(0, src_path)

print(sys.path)
