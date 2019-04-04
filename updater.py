"""
This module provide functions for updating softeware.
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from shutil import copyfile
from logger import *
from sys import exit

root = None
path = os.fspath('//Eapac.ERICSSON.SE/ECNNJDFS01/groups/Group_EN/PTD/23_Team_C/ewngshn')


def check_version():
    """
    Get the newest version on the server.
    """
    try:
        a = os.listdir(path)
        version = ''
        for name in a:
            logger().debug(name)
            if name.startswith('version'):
                version = name.split('_')[1]
                break
        return version
    except FileNotFoundError:
        logger().warning("Update path not exist %s" % path)
        exit(0)


def fetch_update(ver):
    """
    Download new version of the file to local disk.
    Arguments:
        ver - the version of the file to download.
    """
    output_dir = filedialog.askdirectory(title='Select Output Directory')
    if output_dir == '':
        logger().info("Update canceled!")
        return
    try:
        src_path = path + "/db_check_"+ver+".zip"
        dst_path = output_dir + "/db_check_"+ver+".zip"
        copyfile(src_path, dst_path)
        logger().info("Save to : %s" % dst_path)
    except Exception:
        logger().exception("Failed tp download from %s to %s" % (src_path, dst_path))
    return


def run_update(ver):
    """
    Initialize updating process.
    Arguments:
        ver - current version of the tool.
    """
    try:
        global root
        root = tk.Tk()
        root.withdraw()
        init_logger()
        logger().info('Updater start. Current version %s' % ver)
        new_ver = check_version()
        if ver == new_ver:
            logger().info("already newest version!")
        elif new_ver > ver:
            logger().info("New version %s available." % new_ver)
            var_box = messagebox.askyesno(title='DB Check Updater', message='New version available, download now?')
            if var_box:
                fetch_update(new_ver)
            else:
                logger().info("Update canceled!")
        else:
            logger().warning("Version on server is older! This is not normal.")
        return
    except Exception:
        logger().exception("Unexpected error happened in updater!")


def main():
    version = sys.argv[1]
    run_update(version)


if __name__ == '__main__':
    sys.argv.append("1.0")
    main()