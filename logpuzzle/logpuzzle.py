#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
from urllib.request import urlretrieve

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
(animal)
10.254.254.58 - - [06/Aug/2007:00:10:05 -0700] "GET /edu/languages/google-python-class/images/puzzle/a-baaa.jpg HTTP/1.0" 200 2309 "-" "googlebot-mscrawl-moma (enterprise; bar-XYZ; foo123@google.com,foo123@google.com,foo123@google.com,foo123@google.com)"
and
(place)
10.254.254.29 - - [06/Aug/2007:00:12:19 -0700] "GET /edu/languages/google-python-class/images/puzzle/p-bija-baei.jpg HTTP/1.0" 200 22950 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.12) Gecko/20070508 Firefox/1.5.0.12"
Here's the image source:
https://developers.google.com/edu/python/images/puzzle/a-babb.jpg
"""
def second_word(url):
    '''takes a url and parses the last word before the image type (.jpg)
    to be used as a sort key'''
    m = re.search(r'-\w+-(\w+)\.jpg', url)
    return m.group(1)

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    f = open(filename, 'r')
    # a list of grouped-url tuples, the 3d element is the segment of interest
    urls = re.findall(r'GET\s(/[\w-]+)(/[\w-]+)(/[\w-]+)([/\w-]+\.jpg)', f.read())
    f.close()

    # process the url tuples putting the segment + prefix into a unique list
    tmp_list = []
    prefix = 'https://developers.google.com/edu/python'
    for tuple in urls:
        if tuple[3] != 'e.jpg': # exclude bad file(s)
            url = prefix + tuple[3]
            if url not in tmp_list:
                tmp_list.append(url)

    # return a sorted list of complete image urls
    if re.search(r'-\w+-\w+\.jpg', urls[0][3]): # reading the place file
        return sorted(tmp_list, key=second_word)
    else:
        return sorted(tmp_list)

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    # retrieve the image and save to destination
    img_num = 0
    print('retrieving files....')
    for url in img_urls:
        urlretrieve(url, dest_dir + '/img' + str(img_num))
        img_num += 1
    print('done!')

    # create index.html in destination
    html = '<html>\n<head><title>puzzle</title></head>\n</body>\n'
    for i in range(len(img_urls)):
        html += '<img src=\'img' + str(i) + '\'</img>'
    html += '\n</body>\n</html>'

    f = open(dest_dir + '/index.html', 'w')
    f.write(html)
    f.close()

def main():
    args = sys.argv[1:]
    
    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)
    
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]
    
    img_urls = read_urls(args[0])
    
    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))

if __name__ == '__main__':
    main()
