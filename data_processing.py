import re
import utilities as uti
import picture
from logger import *

DUT_S = "DUT"
GOLDEN_S = "Golden"


def req_0(dict_G, dict_D, cmd):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    absence_list = list()
    gd_no_match = False
    legend = list()
    data10 = uti.read_data(dict_D, cmd)
    data10_G = uti.read_data(dict_G, cmd)
    ret_D = True
    ret_G = True

    """
    Plot Golden
    """
    if data10_G is None:
        absence_list.append([cmd, GOLDEN_S])
    else:
        ret_D = picture.plot_fmt_G(data10_G, cmd=cmd, style='p')  # Golden Data (Bottom)
        if ret_D:
            legend.append(GOLDEN_S)
    """
    Plot DUT
    """
    if data10 is None:
        absence_list.append([cmd, DUT_S])
    else:
        ret_G = picture.plot_fmt(data10, cmd=cmd, style='p')  # Current Data (Top)
        if ret_G:
            legend.append(DUT_S)

    if len(absence_list) == 0 and ret_D and ret_G:
        gd_no_match = (len(data10_G) != len(data10))
    """
    Show
    """
    picture.plot_show(cmd, legend=legend, absence_list=absence_list, gd_no_match=gd_no_match)


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
    legend = list()
    absence_list = list()
    gd_no_match = False
    ret_G = True
    ret_D = True

    data10 = uti.read_data(dict_D, cmd)
    data10_G = uti.read_data(dict_G, cmd)
    """
    Plot Golden
    """
    if data10_G is None:
        absence_list.append([cmd, GOLDEN_S])
    else:
        for j in range(len(data10_G)):
            if j % 2 == 0:
                x_G.append(data10_G[j])
            else:
                y1_G.append(data10_G[j])
        ret_G = picture.plot_fmt_G(x_G, y1_G, cmd=cmd)  # Golden Data (Bottom)
        if ret_G:
            legend.append(GOLDEN_S)
    """
    Plot DUT
    """
    if data10 is None:
        absence_list.append([cmd, DUT_S])
    else:
        for j in range(len(data10)):
            if j % 2 == 0:
               x.append(data10[j])
            else:
               y1.append(data10[j])
        ret_D = picture.plot_fmt(x, y1, cmd=cmd)  # Current Data (Top)
        if ret_D:
            legend.append(DUT_S)

    if len(absence_list) == 0 and ret_D and ret_G:
        gd_no_match = (len(data10_G) != len(data10))
    """
    Show
    """
    picture.plot_show(cmd, legend=legend, absence_list=absence_list, gd_no_match=gd_no_match)


def req_2(dict_G, dict_D, cmd_x):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    legend = list()
    absence_list = list()
    gd_no_match = False
    ret_G = True
    ret_D = True
    """
    Read Data
    """
    data10_x = uti.read_data(dict_D, cmd_x)
    data10_x_G = uti.read_data(dict_G, cmd_x)
    cmd_y = cmd_x.replace("_x", "_y")
    data10_y = uti.read_data(dict_D, cmd_y)
    data10_y_G = uti.read_data(dict_G, cmd_y)
    """
    Plot Golden
    """
    if data10_x_G is None:
        absence_list.append([cmd_x, GOLDEN_S])
    if data10_y_G is None:
        absence_list.append([cmd_y, GOLDEN_S])
    if data10_x_G is not None and data10_y_G is not None:
        ret_G = picture.plot_fmt_G(data10_x_G, data10_y_G, cmd=cmd_x)
        if ret_G:
            legend.append(GOLDEN_S)
    """
    Plot DUT
    """
    if data10_x is None:
        absence_list.append([cmd_x, DUT_S])
    if data10_y is None:
        absence_list.append([cmd_y, DUT_S])
    if data10_x is not None and data10_y is not None:
        ret_D = picture.plot_fmt(data10_x, data10_y, cmd=cmd_x)
        if ret_D:
            legend.append(DUT_S)

    # if uti.is_substring("VGLinTable_", cmd_x):
    #     picture.plot_fmt_G(data10_y_G, data10_x_G, cmd=cmd_x)
    #     picture.plot_fmt(data10_y, data10_x, cmd=cmd_x)
    #
    # else:
    #     picture.plot_fmt_G(data10_x_G, data10_y_G, cmd=cmd_x)
    #     picture.plot_fmt(data10_x, data10_y, cmd=cmd_x)
    if len(absence_list) == 0 and ret_D and ret_G:
        gd_no_match = (len(data10_x_G) != len(data10_x))

    picture.plot_show(cmd_x, legend=legend, absence_list=absence_list, gd_no_match=gd_no_match)


def plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re, style=None):
    absence_list = list()
    gd_no_match = False
    mag_G = None
    phase_G = None
    mag = None
    phase = None
    legend = list()
    ret_G = True
    ret_D = True
    """
    Read Data
    """
    data10_fr = uti.read_data(dict_D, cmd_fr)
    data10_fr_G = uti.read_data(dict_G, cmd_fr)
    data10_re = uti.read_data(dict_D, cmd_re)
    data10_re_G = uti.read_data(dict_G, cmd_re)
    data10_im = uti.read_data(dict_D, cmd_im)
    data10_im_G = uti.read_data(dict_G, cmd_im)
    """
    Process Golden Data
    """
    if data10_fr_G is None:
        absence_list.append([cmd_fr, GOLDEN_S])
    if data10_im_G is None:
        absence_list.append([cmd_im, GOLDEN_S])
    if data10_re_G is None:
        absence_list.append([cmd_re, GOLDEN_S])
    if data10_fr_G and data10_im_G and data10_re_G:
        mag_G, phase_G = uti.get_mag_angle(data10_re_G, data10_im_G)
    """
    Process DUT Data
    """
    if data10_fr is None:
        absence_list.append([cmd_fr, DUT_S])
    if data10_im is None:
        absence_list.append([cmd_im, DUT_S])
    if data10_re is None:
        absence_list.append([cmd_re, DUT_S])
    if data10_fr and data10_im and data10_re:
        mag, phase = uti.get_mag_angle(data10_re, data10_im)
    """
    Plot Golden Mag Data
    """
    title = cmd_im.replace('im', 'mag')
    if mag_G is not None:
        ret_G = picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title, style=style)
        if ret_G:
            legend.append('mag-freq_G')
    """
    Plot DUT Mag Data
    """
    if mag is not None:
        ret_D = picture.plot_fmt(data10_fr, mag, cmd=title, style=style)
        if ret_D:
            legend.append('mag-freq')
    """
    Show
    """
    if len(absence_list) == 0 and ret_D and ret_G:
        gd_no_match = (len(data10_fr) != len(data10_fr_G))
    picture.plot_show(title, legend=legend, xlabel="freq", ylabel="mag",
                      absence_list=absence_list, gd_no_match=gd_no_match)
    """
    Plot Golden Phase Data
    """
    title = cmd_im.replace('im', 'phase')
    legend.clear()
    if phase_G is not None:
        ret_G = picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title, style=style)
        if ret_G:
            legend.append('phase-freq_G')
    """
    Plot DUT Phase Data
    """
    if phase is not None:
        ret_D = picture.plot_fmt(data10_fr, phase, cmd=title, style=style)
        if ret_D:
            legend.append('phase-freq')
    """
    Show
    """
    picture.plot_show(title, legend=legend, xlabel="freq", ylabel="phase",
                      absence_list=absence_list, gd_no_match=gd_no_match)


def req_3(dict_G, dict_D, cmd_im):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    cmd_fr = cmd_im.replace("im", "freq")
    cmd_re = cmd_im.replace("im", "re")
    plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re)


def req_4(dict_G, dict_D, cmd_re):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    str = re.compile('[a|b|c]/re')
    cmd_fr = str.sub('abcCal/freq', cmd_re)
    cmd_im = cmd_re.replace("re", "im")
    plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re, style='l')


def req_5(dict_G, dict_D, cmd):
    absence_list = list()
    gd_no_match = False

    data = uti.read_data(dict_D, cmd)
    data_G = uti.read_data(dict_G, cmd)

    if data is None:
        absence_list.append([cmd, DUT_S])
        str_D = list()
    else:
        str_D = re.split(r"\s+", data[0])

    if data_G is None:
        absence_list.append([cmd, GOLDEN_S])
        str_G = list()
    else:
        str_G = re.split(r"\s+", data_G[0])

    comp_res = {}
    for s in str_G:
        comp_res[s.strip()] = 1
    for s in str_D:
        if s.strip() in comp_res:
            comp_res[s.strip()] = 3
        else:
            comp_res[s.strip()] = 2

    t_data = list()
    t_data.append([DUT_S, GOLDEN_S, "Result"])
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
    # print(t_data)
    picture.table_show(cmd, t_data, absence_list=absence_list)


