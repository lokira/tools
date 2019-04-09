import re
import numpy
import utilities as uti
import picture
from logger import *
from tkinter import messagebox

def req_0(dict_G, dict_D, cmd):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    data10 = []
    data10_G = []

    sValue = uti.read_data(dict_D, cmd)
    sValue_G = uti.read_data(dict_G, cmd)

    if uti.is_data_empty(sValue_G, sValue, cmd):
        return

    data10 = uti.trans_data(sValue)
    data10_G = uti.trans_data(sValue_G)
    picture.plot_fmt_G(data10_G, cmd=cmd, style='p')  # Golden Data (Bottom)
    picture.plot_fmt(data10, cmd=cmd, style='p')  # Current Data (Top)

    picture.plot_show(cmd)


def req_1(dict_G, dict_D, cmd):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    x = []
    x_G = []
    y1 = []
    y1_G = []

    values = uti.read_data(dict_D, cmd)
    values_G = uti.read_data(dict_G, cmd)

    if uti.is_data_empty(values_G, values, cmd):
        return

    data10 = uti.trans_data(values)
    data10_G = uti.trans_data(values_G)

    for j in range(len(data10)):
        if j % 2 == 0:
           x.append(data10[j])
        else:
           y1.append(data10[j])

    for j in range(len(data10_G)):
        if j % 2 == 0:
           x_G.append(data10_G[j])
        else:
           y1_G.append(data10_G[j])

    picture.plot_fmt_G(x_G, y1_G, cmd=cmd)  # Golden Data (Bottom)
    picture.plot_fmt(x, y1, cmd=cmd)  # Current Data (Top)
    """
    if uti.is_substring("freq", cmd) or (uti.is_substring("Att", cmd)):
        picture.plot_fmt_G(y1_G, x_G, cmd=cmd)  # Golden Data (Bottom)
        picture.plot_fmt(y1, x, cmd=cmd)  # Current Data (Top)
    else:
        picture.plot_fmt_G(x_G, y1_G, cmd=cmd)  # Golden Data (Bottom)
        picture.plot_fmt(x, y1, cmd=cmd)  # Current Data (Top)
    """
    picture.plot_show(cmd)


def req_2(dict_G, dict_D, cmd_x):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    values_x = uti.read_data(dict_D, cmd_x)
    values_x_G = uti.read_data(dict_G, cmd_x)

    if uti.is_data_empty(values_x_G, values_x, cmd_x):
        return

    data10_x = uti.trans_data(values_x)
    data10_x_G = uti.trans_data(values_x_G)

    cmd_y = cmd_x.replace("_x", "_y")
    values_y = uti.read_data(dict_D, cmd_y)
    values_y_G = uti.read_data(dict_G, cmd_y)

    if uti.is_data_empty(values_y_G, values_y, cmd_y):
        return

    data10_y = uti.trans_data(values_y)
    data10_y_G = uti.trans_data(values_y_G)

    if uti.is_substring("VGLinTable_", cmd_x):
        picture.plot_fmt_G(data10_y_G, data10_x_G, cmd=cmd_x)
        picture.plot_fmt(data10_y, data10_x, cmd=cmd_x)

    else:
        picture.plot_fmt_G(data10_x_G, data10_y_G, cmd=cmd_x)
        picture.plot_fmt(data10_x, data10_y, cmd=cmd_x)

    picture.plot_show(cmd_x)


def req_3(dict_G, dict_D, cmd_im):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    values = []
    values_G = []

    cmd_fr = cmd_im.replace("im", "freq")
    values_fr = uti.read_data(dict_D, cmd_fr)
    values_fr_G = uti.read_data(dict_G, cmd_fr)

    if uti.is_data_empty(values_fr_G, values_fr, cmd_fr):
        return

    data10_fr = uti.trans_data(values_fr)
    data10_fr_G = uti.trans_data(values_fr_G)

    cmd_re = cmd_im.replace("im", "re")
    values_re = uti.read_data(dict_D, cmd_re)
    values_re_G = uti.read_data(dict_G, cmd_re)

    if uti.is_data_empty(values_re_G, values_re, cmd_re):
        return

    data10_re = uti.trans_data(values_re)
    data10_re_G = uti.trans_data(values_re_G)

    values_im = uti.read_data(dict_D, cmd_im)
    values_im_G = uti.read_data(dict_G, cmd_im)

    if uti.is_data_empty(values_im_G, values_im, cmd_im):
        return

    data10_im = uti.trans_data(values_im)
    data10_im_G = uti.trans_data(values_im_G)

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag = 20 * numpy.log10(numpy.absolute(values) / 10e3)
    phase = numpy.angle(values)

    for i in range(len(values_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G = 20 * numpy.log10(numpy.absolute(values_G) / 10e3)
    phase_G = numpy.angle(values_G)

    title = cmd_im.replace('im', 'mag')
    picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title)
    picture.plot_fmt(data10_fr, mag, cmd=title)
    picture.plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag")

    title = cmd_im.replace('im', 'phase')
    picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title)
    picture.plot_fmt(data10_fr, phase, cmd=title)
    picture.plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase")


def req_4(dict_G, dict_D, cmd_re):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    values = []
    values_G = []

    str = re.compile('[a|b|c]/re')
    cmd_fr = str.sub('abcCal/freq', cmd_re)
    values_fr = uti.read_data(dict_D, cmd_fr)
    values_fr_G = uti.read_data(dict_G, cmd_fr)

    if uti.is_data_empty(values_fr_G, values_fr, cmd_fr):
        return

    data10_fr = uti.trans_data(values_fr)
    data10_fr_G = uti.trans_data(values_fr_G)

    values_re = uti.read_data(dict_D, cmd_re)
    values_re_G = uti.read_data(dict_G, cmd_re)

    if uti.is_data_empty(values_re_G, values_re, cmd_re):
        return

    data10_re = uti.trans_data(values_re)
    data10_re_G = uti.trans_data(values_re_G)

    cmd_im = cmd_re.replace("re", "im")
    values_im = uti.read_data(dict_D, cmd_im)
    values_im_G = uti.read_data(dict_G, cmd_im)

    if uti.is_data_empty(values_im_G, values_im, cmd_im):
        return

    data10_im = uti.trans_data(values_im)
    data10_im_G = uti.trans_data(values_im_G)

    if len(data10_re) != len(data10_im):
        logger().info("The length of re and im should be same.")
        return

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag = 20 * numpy.log10(numpy.absolute(values) / 10e3)
    phase = numpy.angle(values)

    if len(data10_re_G) != len(data10_im_G):
        logger().info("The length of re and im in golden file should be same.")
        return

    for i in range(len(values_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G = 20 * numpy.log10(numpy.absolute(values_G) / 10e3)
    phase_G = numpy.angle(values_G)

    title = cmd_im.replace('im', 'mag')
    picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title, style='l')
    picture.plot_fmt(data10_fr, mag, cmd=title, style='l')
    picture.plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag")

    title = cmd_im.replace('im', 'phase')
    picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title, style='l')
    picture.plot_fmt(data10_fr, phase, cmd=title, style='l')
    picture.plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase")





