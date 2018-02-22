#!/usr/bin/python

from celery import Celery, Task
from celery.utils.log import get_task_logger
import platform
import time
import os
import sys
import subprocess
import platform

redis_url = os.environ['REDIS_URL']
swath_mnt_dir = os.environ.get('SWATH_MNT_DIR', None)

hostname = platform.node()
appname = __name__

app = Celery(appname, backend=redis_url, broker=redis_url)

logger = get_task_logger(__name__.upper())

def log(msg):
    global logger
    logger.warning(msg)

class CmdTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if hasattr(exc, 'output'):
            log(exc.output)
        else:
            log(exc.message)

        cmd = args[0]
        if type(cmd) is list:
            cmd = ' '.join(cmd)

        log("COMMAND '%s' FAILED" % cmd)

    def on_success(self, retval, task_id, args, kwargs):
        cmd = args[0]
        if type(cmd) is list:
            cmd = ' '.join(cmd)

        log("COMMAND '%s' SUCCEEDED" % cmd)

@app.task(base=CmdTask)
def run_cmd(cmd):

    log("COMMAND '%s'" % ' '.join(cmd))

    # it's hard to use subprocess.call to redirect output to docker service logs.
    # it had been tried to set stdout=sys.stdout, sys.stdout.fileno(), or subprocess.STDOUT
    # ret = subprocess.call(cmd, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)

    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    log(output)

    return 0
