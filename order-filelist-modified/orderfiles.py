# These days, web servers often send you a randomized hash of the name of the file you're downloading.
# This code is useful for sorting files by modified time in this situations.
#
# It converts the filename to yyyyMMdd-HHmmss format.
# Be careful. this code changes all filename in folder, and original filename will be lost.
# So this code is not recommended if you have files with meaningful filenames.
#
# usage
# 1. Copy this file into folder you want.
# 2. Type below
#      > python3 orderfiles.py
# *. This code supports target folder path with one argument.

import sys
import os
from os.path import isfile, join
import glob
import json
import shutil
import datetime

def orderfiles(inputDir):

    inputPath = os.path.relpath(inputDir)
    files = os.listdir(inputPath)
    
    for oldfile in files:
        moddate = os.path.getmtime(oldfile)
        oldname, oldext = os.path.splitext(oldfile)
        timestamp = datetime.datetime.fromtimestamp(moddate)
        newname = timestamp.strftime("%Y%m%d-%H%M%S") + oldext
        os.rename(oldfile, newname)

    return

if len(sys.argv) < 2:
    orderfiles("./")
else:
    orderfiles(sys.argv[1])

