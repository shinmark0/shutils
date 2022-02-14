# This code is created for rename screen recording files on iOS device.
#
# iOS device creates screen recording file names using epoch time,
# (However, when record is too long, iOS device creates filenames using standard datetime format)
# and do not create meta info into files about creation time.
# So we can't recognize file creation time easily.
# This code converts epoch time based filename to yyyyMMdd-HHmmss format.
#
# basic usage
# 1. Pipe filenames you want convert to converter.py
# 
# simple usage
# 1. copy this file into folder where video files to convert filename are.
# 2. type below
#      > ls | python3 converter.py
#    if you want to filter mp4 extension,
#      > ls *.mp4 | python3 converter.py

import sys
import os
from os.path import isfile, join
import glob
import json
import shutil
import datetime

apple_sr_header = "RPReplay_Final"

def convert1970todate(filename):

    if filename.startswith(apple_sr_header) == False :
        print("file.notmatch: " + filename)
        return

    time1970strext = filename[len(apple_sr_header):]
    time1970str, extstr = os.path.splitext(time1970strext) 

    datetime_name = datetime.datetime.fromtimestamp(int(time1970str))
    datetime_filestr = datetime_name.strftime("%Y%m%d-%H%M%S") + extstr
    
    basepath = os.getcwd()
    if os.path.isfile(datetime_filestr):
        print("failed to rename: [" + datetime_filestr + "] already exists.")
    else:
        os.rename(filename, datetime_filestr)
        print("file.find: [" + filename + "] to [" + datetime_filestr + "]")

    return

while True:
    try:
        convert1970todate(input())
    except EOFError:
        break


