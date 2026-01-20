#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(mydir):
    path_list = []
    if os.path.exists(mydir):
        files = os.listdir(mydir)
        for file in files:
            if re.match(r'.*__\w+__.*', file):
                path = os.path.join(mydir, file)
                path_list.append(os.path.abspath(path))
    else:
        print('directory', mydir, 'does not exist')
        sys.exit(1)
    return path_list

def copy_to(paths, mydir):
    if not os.path.exists(mydir):
        os.mkdir(mydir)
    for file in paths:
        shutil.copy(file, mydir)

def zip_to(paths, zippath):
    cmd = 'zip -j ' + zippath
    for file in paths:
        cmd += ' ' + file + ' '
    print('cmd:', cmd)
    (status, output) = subprocess.getstatusoutput(cmd)
    if status: # something went wrong
        sys.stderr.write(output)
        sys.exit(status)
    print(output)

def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.
    
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print('usage: [--todir dir][--tozip zipfile] dir [dir ...]')
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if not args: # A zero length array evaluates to "False".
        print('error: must specify one or more dirs')
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    paths = get_special_paths(args[0])
    if todir:
        copy_to(paths, todir)
    if tozip:
        zip_to(paths, tozip)

if __name__ == '__main__':
    main()
