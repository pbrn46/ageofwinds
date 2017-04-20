"""
Usage: setup-py2exe.py py2exe
"""

import sys
import os
from distutils.core import setup
import py2exe

sys.path.append('ageofwinds')
os.chdir('ageofwinds')
data_files = []
search_dir = os.path.join('assets')
for root, dirs, files in os.walk(search_dir):
    for f in files:
        p = os.path.join(root, f)
        p = os.path.abspath(p)
        df = root, [p]
        data_files.append(df)
        print root
        print p

os.chdir('..')

# sys.exit(0)

setup(
    windows=[{"script": "ageofwinds/__init__.py", "dest_base": "ageofwinds"}],
    options={
        "py2exe": {
            "includes": ["PySide.QtCore", "PySide.QtGui"],
            "dll_excludes": ["MSVCP90.dll"],
            "dist_dir": "dist-py2exe",
            # "bundle_files": 2
        }
    },
    data_files=data_files
)
