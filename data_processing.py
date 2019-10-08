import re
import utilities as uti
from logger import *
from check_entry import *

DUT_S = "DUT"
GOLDEN_S = "Golden"
CMD_NOT_FOUND_S = "Command not found in %s : %s"
GD_NOT_MATCH_S = "The number of values is different between Golden and DUT data!"
XY_NOT_MATCH_S = "Failed to plot %s %s. \nProbably because the number of x and y values are not match."


def req_0(dict_G, dict_D, cmd, check_entry_list):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    data10 = uti.read_data(dict_D, cmd)
    data10_G = uti.read_data(dict_G, cmd)

    entry = CheckEntry(cmd, CheckEntry.Y)

    if data10_G is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd))
    else:
        entry.load_data_G(data10_G)

    if data10 is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd))
    else:
        entry.load_data(data10)

    if data10 and data10_G and len(data10_G) != len(data10):
        entry.add_err_msg(GD_NOT_MATCH_S)

    check_entry_list.append(entry)


def req_1(dict_G, dict_D, cmd, check_entry_list):
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

    entry = CheckEntry(cmd, CheckEntry.XY)
    """
    Plot Golden
    """
    if data10_G is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd))
    else:
        for j in range(len(data10_G)):
            if j % 2 == 0:
                x_G.append(data10_G[j])
            else:
                y1_G.append(data10_G[j])
        if not (uti.is_same_len(x_G, y1_G)):
            entry.add_err_msg(XY_NOT_MATCH_S % (GOLDEN_S, cmd))
        else:
            entry.load_data_G([x_G, y1_G])
    """
    Plot DUT
    """
    if data10 is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd))
    else:
        for j in range(len(data10)):
            if j % 2 == 0:
               x.append(data10[j])
            else:
               y1.append(data10[j])
        if not (uti.is_same_len(x, y1)):
            entry.add_err_msg(XY_NOT_MATCH_S % (DUT_S, cmd))
        else:
            entry.load_data([x, y1])

    if data10_G and data10 and len(data10_G) != len(data10):
        entry.add_err_msg(GD_NOT_MATCH_S)

    check_entry_list.append(entry)


def req_2(dict_G, dict_D, cmd_x, check_entry_list):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    """
    Read Data
    """
    data10_x = uti.read_data(dict_D, cmd_x)
    data10_x_G = uti.read_data(dict_G, cmd_x)
    cmd_y = cmd_x.replace("_x", "_y")
    data10_y = uti.read_data(dict_D, cmd_y)
    data10_y_G = uti.read_data(dict_G, cmd_y)

    entry = CheckEntry(cmd_x, CheckEntry.XY)
    """
    Plot Golden
    """
    if data10_x_G is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_x))
    if data10_y_G is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_y))
    if data10_x_G is not None and data10_y_G is not None:
        if not uti.is_same_len(data10_x_G, data10_y_G):
            entry.add_err_msg(XY_NOT_MATCH_S % (GOLDEN_S, cmd_x))
        else:
            entry.load_data_G([data10_x_G, data10_y_G])
    """
    Plot DUT
    """
    if data10_x is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_x))
    if data10_y is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_y))
    if data10_x is not None and data10_y is not None:
        if not uti.is_same_len(data10_x, data10_y):
            entry.add_err_msg(XY_NOT_MATCH_S % (DUT_S, cmd_x))
        else:
            entry.load_data([data10_x, data10_y])

    if uti.is_same_len(entry.get_data(), entry.get_data_G()) and len(entry.get_data()):
        if not uti.is_same_len(entry.get_data()[0], entry.get_data_G()[0]):
            entry.add_err_msg(GD_NOT_MATCH_S)

    check_entry_list.append(entry)
    # picture.plot_show(cmd_x, legend=legend, absence_list=absence_list, gd_no_match=gd_no_match)


def plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re, check_entry_list, style=None):
    """
    Read Data
    """
    data10_fr = uti.read_data(dict_D, cmd_fr)
    data10_fr_G = uti.read_data(dict_G, cmd_fr)
    data10_re = uti.read_data(dict_D, cmd_re)
    data10_re_G = uti.read_data(dict_G, cmd_re)
    data10_im = uti.read_data(dict_D, cmd_im)
    data10_im_G = uti.read_data(dict_G, cmd_im)

    title_mag = cmd_im.replace('im', 'mag')
    entry_mag = CheckEntry(title_mag, CheckEntry.XY)
    title_phase = cmd_im.replace('im', 'phase')
    entry_phase = CheckEntry(title_phase, CheckEntry.XY)

    """
    Process Golden Data
    """
    if data10_fr_G is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_fr))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_fr))
    if data10_im_G is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_im))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_im))
    if data10_re_G is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_re))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd_re))

    if data10_fr_G and data10_im_G and data10_re_G:
        if not (uti.is_same_len(data10_fr_G, data10_re_G) and uti.is_same_len(data10_fr_G, data10_im_G)):
            entry_mag.add_err_msg(XY_NOT_MATCH_S % (GOLDEN_S, title_mag))
            entry_phase.add_err_msg(XY_NOT_MATCH_S % (GOLDEN_S, title_phase))
        else:
            mag_G, phase_G = uti.get_mag_angle(data10_re_G, data10_im_G)
            entry_mag.load_data_G([data10_fr_G, mag_G])
            entry_phase.load_data_G([data10_fr_G, phase_G])
    """
    Process DUT Data
    """
    if data10_fr is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_fr))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_fr))
    if data10_im is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_im))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_im))
    if data10_re is None:
        entry_mag.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_re))
        entry_phase.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd_re))

    if data10_fr and data10_im and data10_re:
        if not (uti.is_same_len(data10_fr, data10_re) and uti.is_same_len(data10_fr, data10_im)):
            entry_mag.add_err_msg(XY_NOT_MATCH_S % (DUT_S, title_mag))
            entry_phase.add_err_msg(XY_NOT_MATCH_S % (DUT_S, title_phase))
        else:
            mag, phase = uti.get_mag_angle(data10_re, data10_im)
            entry_mag.load_data([data10_fr, mag])
            entry_phase.load_data([data10_fr, phase])

    if uti.is_not_same_len_not_empty(entry_mag.get_data(), entry_mag.get_data_G()):
        entry_mag.add_err_msg(GD_NOT_MATCH_S)
        entry_phase.add_err_msg(GD_NOT_MATCH_S)

    entry_mag.xlabel = 'freq'
    entry_mag.ylabel = 'mag'

    entry_phase.xlabel = 'freq'
    entry_phase.ylabel = 'phase'

    check_entry_list.append(entry_mag)
    check_entry_list.append(entry_phase)

    #
    # """
    # Plot Golden Mag Data
    # """
    # if mag_G is not None:
    #     ret_G = picture.plot_fmt_G(data10_fr_G, mag_G, cmd=title_mag, style=style)
    #     if ret_G:
    #         legend.append('mag-freq_G')
    # """
    # Plot DUT Mag Data
    # """
    # if mag is not None:
    #     ret_D = picture.plot_fmt(data10_fr, mag, cmd=title_mag, style=style)
    #     if ret_D:
    #         legend.append('mag-freq')
    # """
    # Show
    # """
    # if len(absence_list) == 0 and ret_D and ret_G:
    #     gd_no_match = (len(data10_fr) != len(data10_fr_G))
    # picture.plot_show(title_mag, legend=legend, xlabel="freq", ylabel="mag",
    #                   absence_list=absence_list, gd_no_match=gd_no_match)
    # """
    # Plot Golden Phase Data
    # """
    # title = cmd_im.replace('im', 'phase')
    # legend.clear()
    # if phase_G is not None:
    #     ret_G = picture.plot_fmt_G(data10_fr_G, phase_G, cmd=title_phase, style=style)
    #     if ret_G:
    #         legend.append('phase-freq_G')
    # """
    # Plot DUT Phase Data
    # """
    # if phase is not None:
    #     ret_D = picture.plot_fmt(data10_fr, phase, cmd=title_phase, style=style)
    #     if ret_D:
    #         legend.append('phase-freq')
    # """
    # Show
    # """
    # picture.plot_show(title_phase, legend=legend, xlabel="freq", ylabel="phase",
    #                   absence_list=absence_list, gd_no_match=gd_no_match)


def req_3(dict_G, dict_D, cmd_im, check_entry_list):
    """
    get dut and golden data,draw data picture.
        Arguments:
            dict_G - The dictionary contains commands and data.
            dict_D - The dictionary contains commands and data.
            cmd -  The command to search.
    """
    cmd_fr = cmd_im.replace("im", "freq")
    cmd_re = cmd_im.replace("im", "re")
    plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re, check_entry_list)


def req_4(dict_G, dict_D, cmd_re, check_entry_list):
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
    plot_mag_phase(dict_G, dict_D, cmd_fr, cmd_im, cmd_re, check_entry_list, style='l')


def req_5(dict_G, dict_D, cmd, check_entry_list):

    data = uti.read_data(dict_D, cmd)
    data_G = uti.read_data(dict_G, cmd)
    entry = CheckEntry(cmd, CheckEntry.TABLE)

    if data is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (DUT_S, cmd))
        str_D = list()
    else:
        str_D = re.split(r"\s+", data[0])

    if data_G is None:
        entry.add_err_msg(CMD_NOT_FOUND_S % (GOLDEN_S, cmd))
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
    #t_data.append([DUT_S, GOLDEN_S, "Result"])
    idx = 0
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

    entry.load_t_data(t_data)
    check_entry_list.append(entry)

    # picture.table_show(cmd, t_data, absence_list=absence_list)


