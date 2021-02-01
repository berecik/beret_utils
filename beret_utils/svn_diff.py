#!/usr/bin/env python
import os
import subprocess
import sys
from xml.dom.minidom import parseString


def getXmlData(cmd):
    xml_diff = subprocess.getoutput(cmd)
    xml_diff = xml_diff[xml_diff.find("<?"):]
    return parseString(xml_diff)


def getCmd(src, rev_begin, rev_end):
    if src[:7] == 'http://':
        url = src
        cmd = "svn diff --summarize --xml -r %(rbegin)s:%(rend)s %(url)s" % {'url':  url, 'rbegin': str(rev_begin),
                                                                             'rend': str(rev_end)
        }
    else:
        dir = os.path.abspath(src)
        if not os.path.isdir(dir):
            dir = os.path.dirname(dir)
        cmd = "svn diff --summarize --xml -r %(rbegin)s:%(rend)s %(dir)s" % {'dir':  dir, 'rbegin': str(rev_begin),
                                                                             'rend': str(rev_end)
        }
    return cmd


def getFiles(xml_data):
    files = []
    nodes = xml_data.getElementsByTagName("path")
    for node in nodes:
        if node.attributes['item'].value != "deleted":
            files.append(node.childNodes[0].data)
    return files


def crateDestByDir(dir, dest, files):
    dest = os.path.abspath(dest)
    files = map(lambda file: os.path.abspath(file)[len(dir):], files)
    for file in files:
        src_file = os.path.abspath(dir + os.path.sep + file)
        desc_file = os.path.abspath(dest + os.path.sep + file)
        desc_dir = os.path.dirname(desc_file)
        if not os.path.exists(desc_dir):
            os.makedirs(desc_dir)
        cmd = "cp -vf %s %s" % (src_file, desc_file)
        print(subprocess.getoutput(cmd))


def crateDestByUrl(url, dest, rev_end, urls):
    dest = os.path.abspath(dest)
    for src_url in urls:
        src_file = src_url[len(url):]
        desc_file = os.path.abspath(dest + os.path.sep + src_file)
        desc_dir = os.path.dirname(desc_file)
        if not os.path.exists(desc_dir):
            os.makedirs(desc_dir)
        cmd = "svn export --force -q -r %(rend)s %(src_url)s %(desc_file)s" % {'src_url':   src_url,
                                                                               'desc_file': desc_file, 'rend': rev_end
        }
        out = subprocess.getoutput(cmd)
        if out:
            print(out)
        print("%s -> %s" % (src_url, desc_file))


if __name__ == '__main__':
    argv = sys.argv
    if argv[1][:7] == 'http://':
        url = argv[1]
        argv.remove(url)
    else:
        url = False
    dest = argv[1]
    rev_begin = argv[2]
    rev_end = argv[3] if len(argv) > 3 else 'HEAD'
    if len(argv) > 4:
        dir = argv[4]
    elif not url:
        dir = os.path.abspath('.')
    else:
        dir = False

    src = url if url else dir
    cmd = getCmd(src, rev_begin, rev_end)

    print(cmd)

    data = getXmlData(cmd)
    files = getFiles(data)
    if dir:
        crateDestByDir(dir, dest, files)
    elif url:
        crateDestByUrl(url, dest, rev_end, files)
