"""
This module includes methods that commonly used.
"""
import re
import sys
import os
from logger import *
from tkinter import messagebox

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
    y1 = []
    index_list = []
    dictionary = {}

    wrong_patten = re.compile(r'<|>|Fatal|error|ERROR')
    wrong_flag = 0
    prev_line = ""
    line_no = 0
    for line in f:
        line_no += 1
        data = line.strip()
        # Deal with deviant lines
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

        if data.startswith('$') or data.startswith('#'):
            continue
        elif wrong_patten.search(data):
            logger().warning("Line %s has wrong patten: %s, process together with next line.", line_no, data)
            wrong_flag = 1
            prev_line = data
            continue

        data = data.split('\n')

        for i in range(len(data)):
            if "/" in data[i]:
                data1 = data[i].strip().split(" ")
                y1.append(data1[0])
            else:
                data2 = data[i].strip().split(",")

                for j in range(len(data2)):
                    temp_data = data2[j].strip()
                    if temp_data != '':
                        y1.append(temp_data)

    for k in range(len(y1)):
        if is_substring("/", y1[k]):
            index_list.append(k)

    for m in range(len(index_list)):
        key = y1[index_list[m]]
        current_index = index_list[m] + 1
        if m + 1 == len(index_list):
            next_index = len(y1)
        else:
            next_index = index_list[m + 1]

        dictionary[key] = y1[current_index:next_index]
    return dictionary


def read_data(dictionary, cmd):
    """
    Read the data of the command in the dictionary.
    Arguments:
        dictionary - The dictionary contains commands and data.
        cmd - The command to search.
        return - The data of the command.
    """
    for key in dictionary.keys():
        if cmd == key:
            output = dictionary[key]
            return output
    logger().error("Failed to find this command: %s" % cmd)
    return


def trans_data(value):
    """
    Convert the data to hexadecimal.
    Arguments:
        value - The data to be converted.
        return - The hexadecimal number.
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
