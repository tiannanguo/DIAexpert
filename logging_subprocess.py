# https://gist.github.com/bgreenlee/1402841/9fa25db412d9d687b8fa554a5c4d649b37bee2da

# Code borrowed from http://stackoverflow.com/questions/6809590/merging-a-python-scripts-subprocess-stdout-and-stderr-while-keeping-them-disti/6810231#6810231

import subprocess
import select

def call(popenargs, logger, stdout_log_level=DEBUG, stderr_log_level=ERROR, **kwargs):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.
    """
    child = subprocess.Popen(popenargs, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)
    poll = select.poll()
    poll.register(child.stdout, select.POLLIN | select.POLLHUP)
    poll.register(child.stderr, select.POLLIN | select.POLLHUP)
    pollc = 2

    events = poll.poll()

    while pollc > 0 and len(events) > 0:
        for rfd, event in events:
            if event & select.POLLIN:
                if rfd == child.stdout.fileno():
                    line = child.stdout.readline()
                    if len(line) > 0:
                        logger.log(stdout_log_level, line[:-1])

                if rfd == child.stderr.fileno():
                    line = child.stderr.readline()
                    if len(line) > 0:
                        logger.log(stderr_log_level, line[:-1])

            if event & select.POLLHUP:
                poll.unregister(rfd)
                pollc -= 1

            if pollc > 0:
                events = poll.poll()

    return child.wait()
