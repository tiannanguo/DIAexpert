#!/usr/bin/python

import os
import sys
import time
from swathcmd import run_cmd

appname = os.path.basename(__file__)[:-3].upper()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1:]
        r = run_cmd.delay(cmd)
        while not r.ready():
            time.sleep(1)

        # r.ready() is True
        if r.successful() and r.get() == 0:
            print "[%s] %s succeeded" % (appname, cmd[0])
        else:
            print "[%s] %s failed"    % (appname, cmd[0])