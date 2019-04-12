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
    data10 = uti.read_data(dict_D, cmd)
    data10_G = uti.read_data(dict_G, cmd)

    if uti.is_data_empty(data10_G, data10, cmd):
        return

    picture.plot_fmt_G(data10_G, cmd=cmd, style='p')  # Golden Data (Bottom)
    picture.plot_fmt(data10, cmd=cmd, style='p')  # Current Data (Top)

    picture.plot_show(cmd, gd_no_match=(len(data10_G) != len(data10)))


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

    data10 = uti.read_data(dict_D, cmd)
    data10_G = uti.read_data(dict_G, cmd)

    if uti.is_data_empty(data10_G, data10, cmd):
        return

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

    picture.plot_show(cmd, gd_no_match=(len(x) != len(x_G)))


def req_2(dict_G, dict_D, cmd_x):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    data10_x = uti.read_data(dict_D, cmd_x)
    data10_x_G = uti.read_data(dict_G, cmd_x)

    if uti.is_data_empty(data10_x_G, data10_x, cmd_x):
        return

    cmd_y = cmd_x.replace("_x", "_y")
    data10_y = uti.read_data(dict_D, cmd_y)
    data10_y_G = uti.read_data(dict_G, cmd_y)

    if uti.is_data_empty(data10_y_G, data10_y, cmd_y):
        return

    if uti.is_substring("VGLinTable_", cmd_x):
        picture.plot_fmt_G(data10_y_G, data10_x_G, cmd=cmd_x)
        picture.plot_fmt(data10_y, data10_x, cmd=cmd_x)

    else:
        picture.plot_fmt_G(data10_x_G, data10_y_G, cmd=cmd_x)
        picture.plot_fmt(data10_x, data10_y, cmd=cmd_x)

    picture.plot_show(cmd_x, gd_no_match=(len(data10_x) != len(data10_x_G)))


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
    data10_fr = uti.read_data(dict_D, cmd_fr)
    data10_fr_G = uti.read_data(dict_G, cmd_fr)

    if uti.is_data_empty(data10_fr_G, data10_fr, cmd_fr):
        return

    cmd_re = cmd_im.replace("im", "re")
    data10_re = uti.read_data(dict_D, cmd_re)
    data10_re_G = uti.read_data(dict_G, cmd_re)

    if uti.is_data_empty(data10_re_G, data10_re, cmd_re):
        return

    data10_im = uti.read_data(dict_D, cmd_im)
    data10_im_G = uti.read_data(dict_G, cmd_im)

    if uti.is_data_empty(data10_im_G, data10_im, cmd_im):
        return

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag = 20 * numpy.log10(numpy.absolute(values) / 10e3)
    phase = numpy.angle(values)

    for i in range(len(data10_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G = 20 * numpy.log10(numpy.absolute(values_G) / 10e3)
    phase_G = numpy.angle(values_G)

    title = cmd_im.replace('im', 'mag')
    picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title)
    picture.plot_fmt(data10_fr, mag, cmd=title)
    picture.plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag",
                      gd_no_match=(len(data10_fr)!=len(data10_fr_G)))

    title = cmd_im.replace('im', 'phase')
    picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title)
    picture.plot_fmt(data10_fr, phase, cmd=title)
    picture.plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase",
                      gd_no_match=(len(data10_fr) != len(data10_fr_G)))


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
    data10_fr = uti.read_data(dict_D, cmd_fr)
    data10_fr_G = uti.read_data(dict_G, cmd_fr)

    if uti.is_data_empty(data10_fr_G, data10_fr, cmd_fr):
        return

    data10_re = uti.read_data(dict_D, cmd_re)
    data10_re_G = uti.read_data(dict_G, cmd_re)

    if uti.is_data_empty(data10_re_G, data10_re, cmd_re):
        return

    cmd_im = cmd_re.replace("re", "im")
    data10_im = uti.read_data(dict_D, cmd_im)
    data10_im_G = uti.read_data(dict_G, cmd_im)

    if uti.is_data_empty(data10_im_G, data10_im, cmd_im):
        return

    if len(data10_re) != len(data10_im):
        logger().error("The length of re and im should be same.")
        return

    for i in range(len(data10_im)):
        values.append(complex(int(data10_re[i]), int(data10_im[i])))

    mag, phase = uti.get_mag_angle(values)

    if len(data10_re_G) != len(data10_im_G):
        logger().error("The length of re and im in golden file should be same.")
        return

    for i in range(len(data10_im_G)):
        values_G.append(complex(int(data10_re_G[i]), int(data10_im_G[i])))

    mag_G, phase_G = uti.get_mag_angle(values_G)

    title = cmd_im.replace('im', 'mag')
    picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title, style='l')
    picture.plot_fmt(data10_fr, mag, cmd=title, style='l')
    picture.plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag",
                      gd_no_match=(len(data10_fr) != len(data10_fr_G)))

    title = cmd_im.replace('im', 'phase')
    picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title, style='l')
    picture.plot_fmt(data10_fr, phase, cmd=title, style='l')
    picture.plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase",
                      gd_no_match=(len(data10_fr) != len(data10_fr_G)))


def req_5(dict_G, dict_D, cmd):

    data = uti.read_data(dict_D, cmd)
    data_G = uti.read_data(dict_G, cmd)

    if uti.is_data_empty(data_G, data, cmd):
        return

    str = re.split(r"\s+", data[0])
    str_G = re.split(r"\s+", data_G[0])

    comp_res = {}
    for s in str_G:
        comp_res[s.strip()] = 1
    for s in str:
        if s.strip() in comp_res:
            comp_res[s.strip()] = 3
        else:
            comp_res[s.strip()] = 2

    t_data = list()
    t_data.append(["DUT", "Golden", "Result"])
    idx = 1
    for item in comp_res:
        t_data.append(["", "", ""])
        if comp_res.get(item) & 2:
            t_data[idx][0] = item
        if comp_res.get(item) & 1:
            t_data[idx][1] = item
        if comp_res.get(item) == 3:
            t_data[idx][2] = "OK"
        else:
            t_data[idx][2] = "NOK"
        idx += 1
    print(t_data)
    picture.table_show(cmd, t_data)


