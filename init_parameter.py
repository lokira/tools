"""
This module includes read & write methods
for parameters used by the program.
"""

from logger import *


def read_last_parameters(filename):
    """
    Read parameters from file.
    Arguments:
        filename - Filename to read from.
    Return Values:
        last_product_number, last_tester, req_filename, path_Golden, path_DUT, output_dir
    """
    parameters = []

    try:
        with open(filename, 'r',  encoding="utf-8") as para_file:
            for m_line in para_file:
                line = m_line.strip()
                if not line:
                    continue

                para = line.split(': ')
                if len(para) != 2:
                    continue
                logger().debug(para)
                parameters.append(para[1])
    except IOError:
        logger().warning("Open %s failed - File does not exist." % filename)

    return parameters


def save_last_parameters(filename, m_product_number, m_tester, m_req_file, m_golden_file, m_dut_file, m_output_dir):
    """
    Save parameters to file.
    Arguments:
        filename - Filename to save.
        m_product_number - Product number.
        m_tester - Tester's name.
        m_req_file - File path of requirement file.
        m_golden_file - File path of golden file.
        m_dut_file - File path of dut data file.
        m_output_dir - File path to save the output pictures and reports.
    """
    try:
        with open(filename, 'w+',  encoding="utf-8") as para_file:
            para_file.write('product number: %s\n' % m_product_number)
            para_file.write('tester: %s\n' % m_tester)
            para_file.write('Requirement File: %s\n' % m_req_file)
            para_file.write('Golden File: %s\n' % m_golden_file)
            para_file.write('DUT File: %s\n' % m_dut_file)
            para_file.write('Output directory: %s\n' % m_output_dir)
    except Exception as e:
        logger().exception("Unexpected error happened!")


if __name__ == '__main__':
    product_number = 'aaa'
    tester = 'bbb'
    req_file = 'C:/req_file_xxx'
    golden_file = 'C:/golden_file_xxx'
    dut_file = 'D:/dut_file_xxx'
    output_dir = 'D:/output_dir_xxx'
    save_last_parameters('lastDBCheckPara.txt', product_number, tester, req_file, golden_file, dut_file, output_dir)
    read_last_parameters('lastDBCheckPara.txt')
