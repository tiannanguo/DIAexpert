#!/usr/bin/python

import sys
import os
import time

if __name__ == '__main__':
    print "----> %s" % os.path.basename(__file__)[:-3]
    p = sys.argv[1]
    if p == 'ok':
        time.sleep(int(sys.argv[2]))
        sys.stdout.write("okkkkkkk\n")
        sys.exit(0)
    if p == 'error':
        sys.stderr.write("errorrrr\n")
        sys.exit(int(sys.argv[2]))
    if p == 'except':
        raise Exception(sys.argv[2])
