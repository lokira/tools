"""
This module includes read & write methods
for parameters used by the program.
"""


def read_last_parameters(filename):
    """
    Read parameters from file.
    Arguments:
        filename - Filename to read from.
    Return Values:
        last_product_number, last_tester, req_filename, path_Golden, path_DUT, output_dir
    """
    parameters =[]
    try:
        para_file = open(filename, 'r')
    except IOError:
        print("Open %s failed - No such file or directory. Create a new one." % filename)
        para_file = open(filename, 'x+')
        para_file.write('product number:\n')
        para_file.write('tester:\n')
        para_file.write('Requirement File:\n')
        para_file.write('Golden File:\n')
        para_file.write('DUT File:\n')
        para_file.write('Output directory:\n')
    else:
        print("Open %s successfully." % filename)

    for m_line in para_file:
        line = m_line.strip()
        if not line:
            continue

        para = line.split(': ')
        if len(para) != 2:
            parameters.append("")
            continue
        print(para)
        parameters.append(para[1])
    para_file.close()

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
    para_file = open(filename, 'w+')
    para_file.write('product number: %s\n' % m_product_number)
    para_file.write('tester: %s\n' % m_tester)
    para_file.write('Requirement File: %s\n' % m_req_file)
    para_file.write('Golden File: %s\n' % m_golden_file)
    para_file.write('DUT File: %s\n' % m_dut_file)
    para_file.write('Output directory: %s\n' % m_output_dir)
    para_file.close()


if __name__ == '__main__':
    product_number = 'aaa'
    tester = 'bbb'
    req_file = 'C:/req_file_xxx'
    golden_file = 'C:/golden_file_xxx'
    dut_file = 'D:/dut_file_xxx'
    output_dir = 'D:/output_dir_xxx'
    save_last_parameters('lastDBCheckPara.txt', product_number, tester, req_file, golden_file, dut_file, output_dir)
    read_last_parameters('lastDBCheckPara.txt')
