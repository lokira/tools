import matplotlib.pyplot as plt
import os
import re


import numpy
import MyPicture as mp
import MyReport as mr
import time

import traceback




def is_substring(s1, s2):
    return s1 in s2


def read_dict(file_path):

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
    for key in adic.keys():
        #print (key)
        if cmdName == key:
            output = adic[key]
            return output


def trans_data(value):
    data10 = []
    digital_patten = re.compile(r'^[+-]?[0-9]+(.)?[0-9]*$|^0[xX][0-9a-fA-F]+$')
    for i in range(len(value)):
        if not digital_patten.match(value[i]):
            break
        if is_substring("0x", value[i]) or is_substring("0X", value[i]):
            data10.append(int(value[i], 16))
        else:
            data10.append(value[i])
    return data10


def plot_fmt_G(*data):
    plt.plot(*data, color='#9DCBE1', marker='o',
             markersize=8, linestyle='-', alpha=0.7, linewidth=1)


def plot_fmt(*data):
    plt.plot(*data, color='#124984', marker='.',
             markersize=6, linestyle=':', linewidth=1)


def plot_0(dict_G, dict_D, cmd):
    data10 = []
    data10_G = []

    sValue = read_data(dict_D, cmd)
    sValue_G = read_data(dict_G, cmd)

    if sValue_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if sValue is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10 = trans_data(sValue)
    data10_G = trans_data(sValue_G)
    plot_fmt_G(data10_G)  # Golden Data (Bottom)
    plot_fmt(data10)  # Current Data (Top)

    plt.legend(['golden', 'dut'])
    plt.grid()
    plt.title(cmd)

    mr.save_output(cmd)
    # clear previous figure
    plt.clf()
    plt.cla()


def plot_1(dict_G, dict_D, cmd):
    x = []
    x_G = []
    y1 = []
    y1_G = []

    values = read_data(dict_D, cmd)
    values_G = read_data(dict_G, cmd)

    if values_G is None:
        print("cmd %s is not found in golden DB file." %cmd)
        return

    if values is None:
        print("cmd %s is not found in new DB file." %cmd)
        return

    data10 = trans_data(values)
    data10_G = trans_data(values_G)

    for j in range(len(data10)):
        if j % 2 != 0:
           x.append(data10[j])
        else:
           y1.append(data10[j])

    for j in range(len(data10_G)):
        if j % 2 != 0:
           x_G.append(data10_G[j])
        else:
           y1_G.append(data10_G[j])

    if is_substring("freq", cmd) or (is_substring("Att", cmd)):
        plot_fmt_G(y1_G, x_G)  # Golden Data (Bottom)
        plot_fmt(y1, x)  # Current Data (Top)
    else:
        plot_fmt_G(x_G, y1_G)  # Golden Data (Bottom)
        plot_fmt(x, y1)  # Current Data (Top)

    plt.legend(['golden', 'dut'])
    plt.xticks(rotation=90)
    # plt.grid()
    plt.title(cmd)

    mr.save_output(cmd)
    # clear previous figure
    plt.clf()
    plt.cla()


def plot_2(dict_G, dict_D, cmd_x):
    values_x = read_data(dict_D, cmd_x)
    values_x_G = read_data(dict_G, cmd_x)

    if values_x_G is None:
        print("cmd %s is not found in golden DB file." % cmd_x)
        return

    if values_x is None:
        print("cmd %s is not found in new DB file." % cmd_x)
        return

    data10_x = trans_data(values_x)
    data10_x_G = trans_data(values_x_G)

    cmd_y = cmd_x.replace("_x", "_y")
    values_y = read_data(dict_D, cmd_y)
    values_y_G = read_data(dict_G, cmd_y)

    if values_y_G is None:
        print("cmd %s is not found in golden DB file." % cmd_y)
        return

    if values_y is None:
        print("cmd %s is not found in new DB file." % cmd_y)
        return

    data10_y = trans_data(values_y)
    data10_y_G = trans_data(values_y_G)

    if is_substring("VGLinTable_", cmd_x):
        plt.plot(data10_y_G, data10_x_G, 'g--', data10_y, data10_x, 'r-')
    else:
        plt.plot(data10_x_G, data10_y_G, 'g--', data10_x, data10_y, 'r-')

    plt.legend(['golden', 'dut'])
    plt.grid()
    plt.title(cmd_x)

    mr.save_output(cmd_x)
    # clear previous figure
    plt.clf()
    plt.cla()


def plot_3(dict_G, dict_D, cmd_im):
    values = []
    values_G = []

    cmd_fr = cmd_im.replace("im", "freq")
    values_fr = read_data(dict_D, cmd_fr)
    values_fr_G = read_data(dict_G, cmd_fr)
    if values_fr_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_fr is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_fr = trans_data(values_fr)
    data10_fr_G = trans_data(values_fr_G)

    cmd_re = cmd_im.replace("im", "re")
    values_re = read_data(dict_D, cmd_re)
    values_re_G = read_data(dict_G, cmd_re)
    if values_re_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_re is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_re = trans_data(values_re)
    data10_re_G = trans_data(values_re_G)

    values_im = read_data(dict_D, cmd_im)
    values_im_G = read_data(dict_G, cmd_im)
    if values_im_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_im is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_im = trans_data(values_im)
    data10_im_G = trans_data(values_im_G)

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag = 20 * numpy.log10(numpy.absolute(values) / 10e3)
    phase = numpy.angle(values)

    for i in range(len(values_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G = 20 * numpy.log10(numpy.absolute(values_G) / 10e3)
    phase_G = numpy.angle(values_G)

    plt.plot(data10_fr_G, mag_G, 'go', data10_fr, mag, 'r.')
    plt.legend(['mag-freq_G', 'mag-freq'])
    plt.grid()
    plt.xlabel("freq")
    plt.ylabel("mag")
    title = cmd_im.replace('im', 'mag')
    plt.title(title)

    mr.save_output(title)
    # clear previous figure
    plt.clf()
    plt.cla()

    plt.plot(data10_fr_G, phase_G, 'go', data10_fr, phase, 'r.')
    plt.legend(['phase-freq_G', 'phase-freq'])
    plt.grid()
    plt.xlabel("freq")
    plt.ylabel("phase")
    title = cmd_im.replace('im', 'phase')
    plt.title(title)

    mr.save_output(title)
    # clear previous figure
    plt.clf()
    plt.cla()


def plot_4(dict_G, dict_D, cmd_re):
    values = []
    values_G = []

    str = re.compile('[a|b|c]/re')
    cmd_fr = str.sub('abcCal/freq', cmd_re)
    values_fr = read_data(dict_D, cmd_fr)
    values_fr_G = read_data(dict_G, cmd_fr)
    if values_fr_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_fr is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_fr = trans_data(values_fr)
    data10_fr_G = trans_data(values_fr_G)

    #cmd_re = cmd_im.replace("im", "re")
    values_re = read_data(dict_D, cmd_re)
    values_re_G = read_data(dict_G, cmd_re)
    if values_re_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_re is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_re = trans_data(values_re)
    data10_re_G = trans_data(values_re_G)

    cmd_im = cmd_re.replace("re", "im")
    values_im = read_data(dict_D, cmd_im)
    values_im_G = read_data(dict_G, cmd_im)
    if values_im_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_im is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_im = trans_data(values_im)
    data10_im_G = trans_data(values_im_G)

    if len(data10_re) != len(data10_im):
        print("The length of re and im should be same.")
        return

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag = 20 * numpy.log10(numpy.absolute(values) / 10e3)
    phase = numpy.angle(values)

    if len(data10_re_G) != len(data10_im_G):
        print("The length of re and im in golden file should be same.")
        return

    for i in range(len(values_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G = 20 * numpy.log10(numpy.absolute(values_G) / 10e3)
    phase_G = numpy.angle(values_G)

    plt.plot(data10_fr_G, mag_G, 'g--', data10_fr, mag, 'r-')
    plt.legend(['mag-freq_G', 'mag-freq'])
    plt.grid()
    plt.xlabel("freq")
    plt.ylabel("mag")
    title = cmd_im.replace('im', 'mag')
    plt.title(title)

    mr.save_output(title)
    # clear previous figure
    plt.clf()
    plt.cla()

    plt.plot(data10_fr_G, phase_G, 'g--', data10_fr, phase, 'r-')
    plt.legend(['phase-freq_G', 'phase-freq'])
    plt.grid()
    plt.xlabel("freq")
    plt.ylabel("phase")
    title = cmd_im.replace('im', 'phase')
    plt.title(title)

    mr.save_output(title)
    # clear previous figure
    plt.clf()
    plt.cla()





