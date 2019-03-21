"""
This module includes methods that commonly used.
"""
import re
import sys


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

    f = open(file_path, "r")
    y1 = []
    indexList = []
    adic = {}

    wrong_patten = re.compile(r'<|>|Fatal|error|ERROR')

    for line in f:
        data = line.strip()
        if data.startswith('$') or data.startswith('#'):
            continue
        elif wrong_patten.search(data):
            print("This line has wrong patten: %s" % data)
            continue

        data = data.split('\n')

        for i in range(len(data)):
            if "/" in data[i]:
                data1 = data[i].strip().split(" ")
                y1.append(data1[0])
            else:
                data2 = data[i].strip().split(",")

                for j in range(len(data2)):
                    tempData = data2[j].strip()
                    if tempData != '':
                        y1.append(tempData)

    for k in range(len(y1)):
        if is_substring("/", y1[k]):
            indexList.append(k)

    for m in range(len(indexList)):
        key = y1[indexList[m]]
        currentIndex = indexList[m] + 1
        if m + 1 == len(indexList):
            nextIndex = len(y1)
        else:
            nextIndex = indexList[m + 1]

        adic[key] = y1[currentIndex:nextIndex]
    return adic


def read_data(adic, cmdName):
    """
    Read the data of the command in the dictionary.
    Arguments:
        adic - The dictionary contains commands and data.
        cmdName - The command to search.
        return - The data of the command.
    """
    for key in adic.keys():
        #print (key)
        if cmdName == key:
            output = adic[key]
            return output


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
            data10.append(value[i])
    return list(map(int, data10))


def open_file(filename):
    """
    Open a file.
    Arguments:
        filename - The file to be opened.
        return - the handler of the opened file.
    """

    try:
        opened_file = open(filename, "r")
    except IOError:
        print("Open %s failed - No such file or directory." %filename)
        sys.exit(1)

    else:
        print("Open %s successfully." %filename)
    return opened_file
