import sys


def read_last_para(filename):
    parameters =[]
    try:
        para_file = open(filename, 'r')
    except IOError:
        print("Open %s failed - No such file or directory." % filename)
        sys.exit(1)
    else:
        print("Open %s successfully." % filename)

    for m_line in para_file:
        line = m_line.strip()
        if not line:
            continue

        para = line.split(': ')
        if len(para) != 2:
            continue
        print(para)
        parameters.append(para[1])
    para_file.close()

    return parameters


def save_last_para(filename, m_product_number, m_tester, m_req_file, m_golden_file, m_dut_file):
    para_file = open(filename, 'w+')
    para_file.write('product number: %s\n' % m_product_number)
    para_file.write('tester: %s\n' % m_tester)
    para_file.write('Requirement File: %s\n' % m_req_file)
    para_file.write('Golden File: %s\n' % m_golden_file)
    para_file.write('DUT File: %s\n' % m_dut_file)
    para_file.close()


if __name__ == '__main__':
    product_number = 'aaa'
    tester = 'bbb'
    req_file = 'C:/req_file_xxx'
    golden_file = 'C:/golden_file_xxx'
    dut_file = 'D:/dut_file_xxx'
    save_last_para('lastDBCheckPara.txt', product_number, tester, req_file, golden_file, dut_file)
    read_last_para('lastDBCheckPara.txt')
