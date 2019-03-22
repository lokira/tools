import main_gui as mg
import utilities as uti
import data_processing as dp
import report
import mail
from logger import *


def main_test():
    try:
        init_logger()
        logger().info("DB Check start.")

        (req_filename, path_Golden, path_DUT) = mg.mainGUI()
        print('path_Golden_: ' + path_Golden)
        print('path_DUT_: ' + path_DUT)
        dict_G = uti.read_dict(path_Golden)
        dict_D = uti.read_dict(path_DUT)

        db_req_file = uti.open_file(req_filename)

        for line in db_req_file:
            if line.startswith('#'):
                continue

            line = line.split(' ')
            if len(line) != 2:
                continue
            value = line[1].strip()
            is_digit = value.isdigit()
            if not is_digit:
                print("%s: %s should be a digit." % (line, value))
                break
            cmd = line[0].strip()
            print(cmd)

            tag = int(value)
            if tag == 0:
                dp.req_0(dict_G, dict_D, cmd)
            elif tag == 1:
                dp.req_1(dict_G, dict_D, cmd)
            elif tag == 2:
                if uti.is_substring("_x", cmd):
                    dp.req_2(dict_G, dict_D, cmd)
                else:
                    continue
            elif tag == 3:
                if uti.is_substring("S21/im", cmd):
                    dp.req_3(dict_G, dict_D, cmd)
                else:
                    continue
            elif tag == 4:
                if uti.is_substring("DVSWR", cmd) and uti.is_substring("/re", cmd):
                    dp.req_4(dict_G, dict_D, cmd)
                else:
                    continue
            else:
                print('This DB format is not supported.')

        db_req_file.close()

        report.generate_test_report()
        mail.send_mail()
    except Exception as e:
        logger().exception("Unexpected error happened!")


if __name__ == '__main__':
    main_test()
