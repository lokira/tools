import matplotlib.pyplot as plt
import os
import re


import numpy
import picture
import report
import time

import traceback

from matplotlib.widgets import Button
from tkinter import simpledialog
from tkinter import messagebox

import utilities as uti


def plot_fmt_G(*data, style='unknown'):
    if style == 'p':
        m_marker = '*'
        m_style = ''
    elif style == 'l':
        m_marker = ''
        m_style = ':'
    else:
        m_marker = '*'
        m_style = ':'

    plt.plot(*data, color='#FB7D07', marker=m_marker,
             markersize=6, linestyle=m_style, alpha=0.7, linewidth=1)


def plot_fmt(*data, style='unknown'):
    if style == 'p':
        m_marker = '.'
        m_style = ''
    elif style == 'l':
        m_marker = ''
        m_style = '-'
    else:
        m_marker = '.'
        m_style = '-'
    plt.plot(*data, color='#0652FF', marker=m_marker,
             markersize=4, linestyle=m_style, linewidth=1)


def plot_show(title, legend=['golden', 'dut'], xlabel=None, ylabel=None, **kwargs):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(legend)
    plt.title(title)
    plt.subplots_adjust(bottom=0.15)
    b_ok = Button(plt.axes([0.7, 0.01, 0.1, 0.05]), 'Correct')
    b_nok = Button(plt.axes([0.82, 0.01, 0.1, 0.05]), 'Wrong')
    b_ok.on_clicked(on_click_func("Correct", title))
    b_nok.on_clicked(on_click_func("Wrong", title))

    plt.show()

    # clear previous figure
    plt.clf()
    plt.cla()


def on_click_func(btn, cmd):
    if btn == "Correct":
        def func(event):
            picture.comments = "Correct"
            report.save_output(cmd)
    else:
        def func(event):
            comment = simpledialog.askstring("Comment Requied", "Please input your comment:")
            if comment and comment.strip():
                picture.comments = comment
                picture.test_result = 0
                report.save_output(cmd)
                print(comment)
            else:
                messagebox.showwarning(title='Warning', message='Please input comments first!')

    return func


def plot_0(dict_G, dict_D, cmd):
    data10 = []
    data10_G = []

    sValue = uti.read_data(dict_D, cmd)
    sValue_G = uti.read_data(dict_G, cmd)

    if sValue_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if sValue is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10 = uti.trans_data(sValue)
    data10_G = uti.trans_data(sValue_G)
    plot_fmt_G(data10_G, style='p')  # Golden Data (Bottom)
    plot_fmt(data10, style='p')  # Current Data (Top)

    plot_show(cmd)



def plot_1(dict_G, dict_D, cmd):
    x = []
    x_G = []
    y1 = []
    y1_G = []

    values = uti.read_data(dict_D, cmd)
    values_G = uti.read_data(dict_G, cmd)

    if values_G is None:
        print("cmd %s is not found in golden DB file." %cmd)
        return

    if values is None:
        print("cmd %s is not found in new DB file." %cmd)
        return

    data10 = uti.trans_data(values)
    data10_G = uti.trans_data(values_G)

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

    if uti.is_substring("freq", cmd) or (uti.is_substring("Att", cmd)):
        plot_fmt_G(y1_G, x_G)  # Golden Data (Bottom)
        plot_fmt(y1, x)  # Current Data (Top)
    else:
        plot_fmt_G(x_G, y1_G)  # Golden Data (Bottom)
        plot_fmt(x, y1)  # Current Data (Top)

    plot_show(cmd)


def plot_2(dict_G, dict_D, cmd_x):
    values_x = uti.read_data(dict_D, cmd_x)
    values_x_G = uti.read_data(dict_G, cmd_x)

    if values_x_G is None:
        print("cmd %s is not found in golden DB file." % cmd_x)
        return

    if values_x is None:
        print("cmd %s is not found in new DB file." % cmd_x)
        return

    data10_x = uti.trans_data(values_x)
    data10_x_G = uti.trans_data(values_x_G)

    cmd_y = cmd_x.replace("_x", "_y")
    values_y = uti.read_data(dict_D, cmd_y)
    values_y_G = uti.read_data(dict_G, cmd_y)

    if values_y_G is None:
        print("cmd %s is not found in golden DB file." % cmd_y)
        return

    if values_y is None:
        print("cmd %s is not found in new DB file." % cmd_y)
        return

    data10_y = uti.trans_data(values_y)
    data10_y_G = uti.trans_data(values_y_G)

    if uti.is_substring("VGLinTable_", cmd_x):
        plot_fmt_G(data10_y_G, data10_x_G)
        plot_fmt(data10_y, data10_x)

    else:
        plot_fmt_G(data10_x_G, data10_y_G)
        plot_fmt(data10_x, data10_y)

    plot_show(cmd_x)


def plot_3(dict_G, dict_D, cmd_im):
    values = []
    values_G = []

    cmd_fr = cmd_im.replace("im", "freq")
    values_fr = uti.read_data(dict_D, cmd_fr)
    values_fr_G = uti.read_data(dict_G, cmd_fr)
    if values_fr_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_fr is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_fr = uti.trans_data(values_fr)
    data10_fr_G = uti.trans_data(values_fr_G)

    cmd_re = cmd_im.replace("im", "re")
    values_re = uti.read_data(dict_D, cmd_re)
    values_re_G = uti.read_data(dict_G, cmd_re)
    if values_re_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_re is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_re = uti.trans_data(values_re)
    data10_re_G = uti.trans_data(values_re_G)

    values_im = uti.read_data(dict_D, cmd_im)
    values_im_G = uti.read_data(dict_G, cmd_im)
    if values_im_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_im is None:
        print("cmd %s is not found in new DB file." % cmd)
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

    plot_fmt_G(data10_fr_G, mag_G)
    plot_fmt(data10_fr, mag)
    title = cmd_im.replace('im', 'mag')
    plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag")

    plot_fmt_G(data10_fr_G, phase_G)
    plot_fmt(data10_fr, phase)
    title = cmd_im.replace('im', 'phase')
    plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase")


def plot_4(dict_G, dict_D, cmd_re):
    values = []
    values_G = []

    str = re.compile('[a|b|c]/re')
    cmd_fr = str.sub('abcCal/freq', cmd_re)
    values_fr = uti.read_data(dict_D, cmd_fr)
    values_fr_G = uti.read_data(dict_G, cmd_fr)
    if values_fr_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_fr is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_fr = uti.trans_data(values_fr)
    data10_fr_G = uti.trans_data(values_fr_G)

    values_re = uti.read_data(dict_D, cmd_re)
    values_re_G = uti.read_data(dict_G, cmd_re)
    if values_re_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_re is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_re = uti.trans_data(values_re)
    data10_re_G = uti.trans_data(values_re_G)

    cmd_im = cmd_re.replace("re", "im")
    values_im = uti.read_data(dict_D, cmd_im)
    values_im_G = uti.read_data(dict_G, cmd_im)
    if values_im_G is None:
        print("cmd %s is not found in golden DB file." % cmd)
        return

    if values_im is None:
        print("cmd %s is not found in new DB file." % cmd)
        return

    data10_im = uti.trans_data(values_im)
    data10_im_G = uti.trans_data(values_im_G)

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

    plot_fmt_G(data10_fr_G, mag_G, style='l')
    plot_fmt(data10_fr, mag, style='l')
    title = cmd_im.replace('im', 'mag')
    plot_show(title, legend=['mag-freq_G', 'mag-freq'], xlabel="freq", ylabel="mag")

    plot_fmt_G(data10_fr_G, phase_G, style='l')
    plot_fmt(data10_fr, phase, style='l')
    title = cmd_im.replace('im', 'phase')
    plot_show(title, legend=['phase-freq_G', 'phase-freq'], xlabel="freq", ylabel="phase")





