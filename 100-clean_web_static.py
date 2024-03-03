#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ['52.91.153.57', '34.227.101.246']


def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)
    if number < 1:
        number = 1

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        archives_to_delete_local = local_archives[:-number]
        [local("rm -f {}".format(archive)) for archive in archives_to_delete_local]

    with cd("/data/web_static/releases"):
        run_archives = run("ls -tr").split()
        web_static_archives = [archive for archive in run_archives if "web_static_" in archive]
        archives_to_delete_remote = web_static_archives[:-number]
        [run("rm -rf {}".format(archive)) for archive in archives_to_delete_remote]
