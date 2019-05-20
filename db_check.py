import updater
import main_gui as mg
import utilities as uti
import data_processing as dp
import mail
from logger import *
from tkinter import messagebox
from multiprocessing import Process
from multiprocessing import freeze_support
from picture import open_check_win
import re


freeze_support()


def main_test():
    """
    Generate main_test functions
    Open mainGUI select the appropriate file
    draw golden and dut data
    send mail
    """
    version = '1.4'
    try:
        init_logger()
        logger().info("DB Check started. Version %s.", version)

        p = Process(target=updater.run_update, args=(version,))
        p.start()

        (req_filename, path_Golden, path_DUT) = mg.mainGUI(version)
        logger().info('path_Golden_: ' + path_Golden)
        logger().info('path_DUT_: ' + path_DUT)
        dict_G = uti.read_dict(path_Golden)
        dict_D = uti.read_dict(path_DUT)

        db_req_file = uti.open_file(req_filename)
        check_entry_list = list()

        req_pattern = re.compile(r"(?P<cmd>[^#]\S+)\s+(?P<tag>[0-5])")  # Not start with '#', tag in 0-5

        for line in db_req_file:
            m = req_pattern.match(line)
            if m is not None:
                cmd = m.group("cmd")
                tag = int(m.group("tag"))
            else:
                logger().warning("%s in requirement file is not in correct format." % line)
                continue

            if tag == 0:
                dp.req_0(dict_G, dict_D, cmd, check_entry_list)
            elif tag == 1:
                dp.req_1(dict_G, dict_D, cmd, check_entry_list)
            elif tag == 2:
                if uti.is_substring("_x", cmd):
                    dp.req_2(dict_G, dict_D, cmd, check_entry_list)
                else:
                    continue
            elif tag == 3:
                if uti.is_substring("S21/im", cmd):
                    dp.req_3(dict_G, dict_D, cmd, check_entry_list)
                else:
                    continue
            elif tag == 4:
                if uti.is_substring("DVSWR", cmd) and uti.is_substring("/re", cmd):
                    dp.req_4(dict_G, dict_D, cmd, check_entry_list)
                else:
                    continue
            elif tag == 5:
                if uti.is_substring("componentConfigId", cmd):
                    dp.req_5(dict_G, dict_D, cmd, check_entry_list)
                else:
                    continue
            else:
                logger().info("This DB format is not supported.")

        db_req_file.close()
        open_check_win(check_entry_list)
        return

    except Exception as e:
        logger().exception("Unexpected error happened!")
        var_box = messagebox.askyesno(title='Warning', message='Unexpected error happened!\nWould you like to send us the log to help us improve?')
        if var_box:
            mail.send_bug_report()


if __name__ == '__main__':
    main_test()
