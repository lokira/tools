
import os
import sys
import time
#import tkinter as tk
#from tkinter import filedialog
#from tkinter import messagebox

#from docx.shared import RGBColor
#from docx import Document

import MainGui as mg
import DataProcessing as dp
import MyMail as mm
#import MyPicture as mp

import MyReport as mr



#from PIL import Image, ImageTk

#from email.mime.text import MIMEText
#from email.mime.image import MIMEImage


'''
document = Document()
document.add_heading('DB CHECK REPORT', level=0)

p = document.add_paragraph('Product number: KRC 161 635/1 R5E')
p = document.add_paragraph('Tester:         Iris')
p = document.add_paragraph('DB Check Date:  2019.2.20') 

p = document.add_paragraph('Test Result:    ')
p.add_run('PASS').font.color.rgb = RGBColor(0x22, 0x8B, 0x22)
p = document.add_paragraph('Conclusion:     This test sw is ok to release.')

document.save('test.docx')
'''
dict_G = {}
dict_D = {}


def open_file(filename):

    try:
        opened_file = open(filename, "r")
    except IOError:
        print("Open %s failed - No such file or directory." %filename)
        sys.exit(1)
    else:
        print("Open %s successfully." %filename)
    return opened_file


def main_test():
    global dict_G
    global dict_D

    '''
    root = tk.Tk()
    root.withdraw()
    
    req_filename = filedialog.askopenfilename(title='select the DB requirement file',
                                              filetypes=[('text file', '*.txt'), ('All Files', '*')])
    path_Golden = filedialog.askopenfilename(title='select the old golden DB file',
                                             filetypes=[('text file', '*.txt'), ('All Files', '*')])

    path_DUT = filedialog.askopenfilename(title='select the new DUT DB file',
                                          filetypes=[('text file', '*.txt'), ('All Files', '*')])

    root.destroy()
    '''
    

    (product_number, tester, req_filename, path_Golden, path_DUT) = mg.mainGUI()
    print('path_Golden_: ' + path_Golden)
    print('path_DUT_: ' + path_DUT)
    dict_G = dp.read_dict(path_Golden)
    dict_D = dp.read_dict(path_DUT)

    '''
    req_filename = os.path.abspath('database_requirement.txt')

    path_Golden = os.path.abspath('golden.txt')
    dict_G = dp.read_dict(path_Golden)

    path_DUT = os.path.abspath('list db prod.txt')
    dict_D = dp.read_dict(path_DUT)
    '''

    mr.create_report(product_number, tester, req_filename, path_Golden, path_DUT)
    db_req_file = open_file(req_filename)

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
            dp.plot_0(dict_G, dict_D, cmd)
        elif tag == 1:
            dp.plot_1(dict_G, dict_D, cmd)
        elif tag == 2:
            if dp.is_substring("_x", cmd):
                dp.plot_2(dict_G, dict_D, cmd)
            else:
                continue
        elif tag == 3:
            if dp.is_substring("S21/im", cmd):
                dp.plot_3(dict_G, dict_D, cmd)
            else:
                continue
        elif tag == 4:
            if dp.is_substring("DVSWR", cmd) and dp.is_substring("/re", cmd):
                dp.plot_4(dict_G, dict_D, cmd)
            else:
                continue
        else:
            print('This DB format is not supported.')

    db_req_file.close()
    mr.add_conclusion()
    mr.add_pictures()

    mm.send_mail()



if __name__ == '__main__':
    main_test()
