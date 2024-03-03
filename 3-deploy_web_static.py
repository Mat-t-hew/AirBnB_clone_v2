#!/usr/bin/python3
"""Distributes an archive to your web servers, using the function do_deploy"""
from fabric.api import env, put, run, local
import time
import os

env.hosts = ['52.91.153.57', '34.227.101.246']

def do_pack():
    """Generate tgz."""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions/web_static")
        local("echo '<html><head></head><body>My Index</body></html>' > versions/web_static/my_index.html")
        local("tar -cvzf versions/web_static_{:s}.tgz -C versions web_static/".format(timestamp))
        return "versions/web_static_{:s}.tgz".format(timestamp)
    except:
        return None

def do_deploy(archive_path):
    """Function for deploy."""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    dest = data_path + name

    try:
        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(dest))
        run('tar -xzf /tmp/{}.tgz -C {}'.format(name, dest))
        run('rm -f /tmp/{}.tgz'.format(name))
        run('mv {}/web_static/* {}/'.format(dest, dest))
        run('rm -rf {}/web_static'.format(dest))
        run('rm -rf /data/web_static/current'.format(name))
        run('ln -s {} /data/web_static/current'.format(dest))
        return True
    except:
        return False

if __name__ == "__main__":
    path = do_pack()
    if path is None:
        print("Packaging failed. Aborting deployment.")
    elif not do_deploy(path):
        print("Deployment failed.")
    else:
        print("Deployment successful.")
