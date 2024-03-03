#!/usr/bin/python3
"""Distributes an archive to your web servers, using the function do_deploy."""
import os
import time
from fabric.api import *

# Define remote hosts
env.hosts = ['52.91.153.57', '34.227.101.246']

def do_pack():
    """Generate a tar gzipped archive of the web_static directory."""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".format(timestamp))
        return "versions/web_static_{:s}.tgz".format(timestamp)
    except Exception as e:
        print(f"Error occurred during packing: {e}")
        return None

def do_deploy(archive_path):
    """Deploy the archive to the remote servers."""
    if not os.path.exists(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False

    try:
        data_path = '/data/web_static/releases/'
        tmp = os.path.basename(archive_path).split('.')[0]
        name = os.path.basename(tmp)
        dest = data_path + name

        put(archive_path, '/tmp')
        run('mkdir -p {}'.format(dest))
        run('tar -xzf /tmp/{}.tgz -C {}'.format(name, dest))
        run('rm -f /tmp/{}.tgz'.format(name))
        run('mv {}/web_static/* {}/'.format(dest, dest))
        run('rm -rf {}/web_static'.format(dest))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(dest))
        print("Deployment successful.")
        return True
    except Exception as e:
        print(f"Error occurred during deployment: {e}")
        return False

def deploy():
    """Compress and upload files to remote server."""
    path = do_pack()
    if path is None:
        print("Packaging failed. Aborting deployment.")
        return False
    return do_deploy(path)

if __name__ == "__main__":
    deploy()
