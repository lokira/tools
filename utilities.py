"""
This module includes methods that commonly used.
"""
import re
import sys
import os
from logger import *
from tkinter import messagebox
import numpy


class DBEntry(object):
    cmd, type, data = None, None, None

    def __init__(self, cmd, type, data=None):
        self.cmd = cmd
        self.type = type
        if type.startswith("U"):
            def f(v):
                return int(v, 16)
            self.trans = f
        elif type.startswith("S"):
            def f(v):
                return int(v)
            self.trans = f
        elif "char" in type or "CHR" in type:
            def f(v):
                return v.strip('"').strip()
            self.trans = f
        if data is None:
            self.data = []

    def append(self, d):
        try:
            self.data.append(self.trans(d.strip()))
        except ValueError:
            logger().warning("Incompatible value %s for %s. ", d, self.cmd)

    def trans(self, v):
        return v


def is_substring(s1, s2):
    """
    Judge if s1 is the substring of s2.
    Arguments:
        s1 - The first string.
        s2 - The second string.
        return - True if s1 is the substring of s2.
                 False if s1 is not the substring of s2.
    """
    return s1 in s2


def read_dict(file_path):
    """
    Read commands and data from a file and save them to a dictionary.
    Commands are the keys of the dictionary while data are the values
    of the dictionary.
    Arguments:
        file_path - The file contains all commands and data.
        return - The dictionary of all commands and data.
    """

    f = open_file(file_path)
    dictionary = {}

    wrong_patten = re.compile(r'<|>|Fatal|error|ERROR')
    wrong_flag = 0
    prev_line = ""
    line_no = 0
    cmd = None
    """
    This pattern matches lines in shape of : 
        1. /cmdline P S32
        2. /cmdline S32
        3. /cmdlineS32
    """
    """
    # Not recognize S E
    pattern = re.compile(r"(?P<cmd>/\S+)\s*[SPE]{0,2}\s*(?P<type>[S|U]8|[S|U]16|[S|U]32|[S|U]64|char)")  
    """
    pattern = re.compile(r"(?P<cmd>/\S+)\s*[SPE\s]{0,3}\s*(?P<type>[S|U]8|[S|U]16|[S|U]32|[S|U]64|char|CHR)")
    for line in f:
        line_no += 1
        data = line.strip()
        # Deal with previous deviant lines
        if wrong_flag == 1:
            data = prev_line+data
            logger().warning("Processing line %s with previous line : %s", line_no, data)
            data = re.sub(u"<.*>", "", data)  # This will remove the <> and content in it
            if data == '':
                logger().warning("No data. Skipped.")
                continue
            logger().warning("After correction: %s" % data)
            wrong_flag = 0
            prev_line = ""
        # skip useless lines
        if data.startswith('$') or data.startswith('#'):
            continue
        elif wrong_patten.search(data):
            logger().warning("Line %s has wrong patten: %s, process together with next line.", line_no, data)
            wrong_flag = 1
            prev_line = data
            continue

        if data.startswith("/"):
            # data1 = re.split(r"\s+", data)
            m = pattern.match(data)
            if m is not None:
                cmd = m.group("cmd")
                entry = DBEntry(cmd, m.group("type"))
                dictionary[cmd] = entry
            else:
                logger().warning("String not match to regex pattern! %s" % data)
        else:
            data2 = data.split(",")
            for j in range(len(data2)):
                temp_data = data2[j].strip()
                if temp_data != '':
                    if cmd in dictionary:
                        dictionary[cmd].append(temp_data)

    return dictionary


def read_data(dictionary, cmd):
    """
    Read the data of the command in the dictionary.
    Arguments:
        dictionary - The dictionary contains commands and data.
        cmd - The command to search.
        return - The data of the command.
    """
    if cmd in dictionary:
        return dictionary[cmd].data
    logger().error("Failed to find this command: %s" % cmd)
    return


def trans_data(value):
    """
    Convert the data to decimal.
    Arguments:
        value - The data to be converted.
        return - The decimal number.
    """
    data10 = []
    digital_patten = re.compile(r'^[+-]?[0-9]+(.)?[0-9]*$|^0[xX][0-9a-fA-F]+$')
    for i in range(len(value)):
        if not digital_patten.match(value[i]):
            break
        if is_substring("0x", value[i]) or is_substring("0X", value[i]):
            data10.append(int(value[i], 16))
        else:
            data10.append(int(value[i]))
    return data10


def open_file(filename):
    """
    Open a file.
    Arguments:
        filename - The file to be opened.
        return - the handler of the opened file.
    """

    try:
        opened_file = open(filename, "r")
    except FileNotFoundError:
        logger().exception("Open %s failed - No such file or directory." % filename)
        messagebox.showerror(title='Error',
                             message='File not exist!\n%s' % filename)
        sys.exit(1)
    except IOError:
        logger().exception("Open %s failed - No such file or directory." % filename)
        sys.exit(1)
    else:
        logger().info("Open %s successfully." % filename)
    return opened_file


def create_dir(directory):
    """
    Create a directory.
    Arguments:
        dir - The directory to be created.
    """
    try:
        logger().debug("try to mkdir %s." % directory)
        os.mkdir(directory)
    except:
        logger().exception("Create directory %s failed for the 1st time." % directory)
        try:
            os.makedirs(directory)
        except:
            logger().exception("Create directory %s failed for the 2nd time." % directory)
        else:
            logger().info("Create directory %s successfully for the 2nd time." % directory)
    else:
        logger().info("Create directory %s successfully for the 1st time." % directory)


def get_mag_angle(real, image):
    """
    Calculate magnitude and phase angle from the real value and image value data array.
    """
    comp_val = list()
    for i in range(len(real)):
        comp_val.append(complex(int(real[i]), int(image[i])))
    mag = 20 * numpy.log10(numpy.absolute(comp_val) / 10e3)
    phase = numpy.angle(comp_val)
    return mag, phase


def is_same_len(arr1, arr2):
    """
    To determine if two arrays have same size.
    """
    return len(arr1) == len(arr2)


def is_not_same_len_not_empty(arr1, arr2):
    """
    To determine if two arrays which are not empty are different in size.
    """
    return len(arr1) and len(arr2) and not is_same_len(arr1, arr2)
