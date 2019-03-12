import time
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
import DBCheckPara as dbcp

root = tk.Tk()

#root.withdraw()
req_entry = tk.Entry(root, width=40)
golden_entry = tk.Entry(root, width=40)
dut_entry = tk.Entry(root, width=40)

#g_product_number = ''
#g_tester = ''
product_number = ''
tester = ''

req_filename = ''
path_Golden = ''
path_DUT = ''


def req_callback():
    global req_entry
    global req_filename
    global product_number
    global tester

    req_filename = filedialog.askopenfilename(title='select the DB requirement file',
                                              filetypes=[('text file', '*.txt'), ('All Files', '*')])
    print(req_filename)
    req_entry.delete(0, tk.END)
    req_entry.insert(0, req_filename)


def golden_callback():
    global golden_entry
    global path_Golden
    path_Golden = filedialog.askopenfilename(title='select the old golden DB file',
                                             filetypes=[('text file', '*.txt'), ('All Files', '*')])
    print(path_Golden)
    golden_entry.delete(0, tk.END)
    golden_entry.insert(0, path_Golden)

def dut_callback():
    global dut_entry
    global path_DUT

    path_DUT = filedialog.askopenfilename(title='select the new DUT DB file',
                                          filetypes=[('text file', '*.txt'), ('All Files', '*')])
    print(path_DUT)
    dut_entry.delete(0, tk.END)
    dut_entry.insert(0, path_DUT)


def confirm_callback():
    global root
    global g_product_number
    global g_tester
    global product_number
    global tester
    global seen

    g_product_number = product_number.get()
    if len(g_product_number) == 0:
        messagebox.showwarning(title='Warning', message='Please input product number!')
        return False

    g_tester = tester.get().lstrip()
    if len(g_tester) == 0:
        messagebox.showwarning(title='Warning', message='Please input tester!')
        return False

    dbcp.save_last_para('lastDBCheckPara.txt', g_product_number, g_tester, req_filename, path_Golden, path_DUT)
    root.quit()

    '''
    root.withdraw()
    time.sleep(10)
    root.update()
    root.deiconify()
    '''

    return


def cancel_callback():
    global root
    print('cancel')
    root.quit()

    return


def mainGUI():
    global root
    global g_product_number
    global g_tester

    global product_number
    global tester
    global req_filename
    global path_Golden
    global path_DUT


    root.title("DBCheck")
    last_product_number, last_tester, req_filename, path_Golden, path_DUT = \
        dbcp.read_last_para('lastDBCheckPara.txt')

    product_number_label = tk.Label(root, text="Product Number:")
    product_number_label.grid(sticky=tk.E, row=0, column=0, columnspan=1, padx=20, pady=10)


    product_number = tk.StringVar()
    product_number_entry = tk.Entry(root, textvariable=product_number, width=30)
    product_number_entry.grid(sticky=tk.W, row=0, column=1, columnspan=2, padx=20, pady=10)

    # last_product_number = 'aaa'
    print(last_product_number)
    product_number_entry.delete(0, tk.END)
    product_number_entry.insert(0, last_product_number)

    tester_label = tk.Label(root, text="Tester:")
    tester_label.grid(sticky=tk.E, row=1, column=0, columnspan=1, padx=20, pady=10)


    tester = tk.StringVar()
    tester_entry = tk.Entry(root, textvariable=tester, width=30)
    tester_entry.grid(sticky=tk.W, row=1, column=1, columnspan=2, padx=20, pady=10)

    print(last_tester)
    tester_entry.delete(0, tk.END)
    tester_entry.insert(0, last_tester)

    req_label = tk.Label(root, text="DB requirement file:")
    req_label.grid(sticky=tk.E, row=2, column=0, columnspan=1, padx=20, pady=10)

    global req_entry
    req_entry = tk.Entry(root, width=80)
    req_entry.grid(row=2, column=1, columnspan=2, padx=20, pady=10)
    req_button = tk.Button(root, text="select", command=req_callback, width=10)
    req_button.grid(sticky=tk.E + tk.N, row=2, column=3, padx=20, pady=10)

    print(req_filename)
    req_entry.delete(0, tk.END)
    req_entry.insert(0, req_filename)

    golden_label = tk.Label(root, text="Golden DB file:")
    golden_label.grid(sticky=tk.E, row=3, column=0, columnspan=1, padx=20, pady=10)

    global golden_entry
    golden_entry = tk.Entry(root, width=80)
    golden_entry.grid(row=3, column=1, columnspan=2, padx=20, pady=10)
    golden_button = tk.Button(root, text="select", command=golden_callback, width=10)
    golden_button.grid(sticky=tk.E + tk.N, row=3, column=3, padx=20, pady=10)

    print(path_Golden)
    golden_entry.delete(0, tk.END)
    golden_entry.insert(0, path_Golden)

    dut_label = tk.Label(root, text="DUT DB file:")
    dut_label.grid(sticky=tk.E, row=4, column=0, columnspan=1, padx=20, pady=10)

    global dut_entry
    dut_entry = tk.Entry(root, width=80)
    dut_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=10)
    dut_button = tk.Button(root, text="select", command=dut_callback, width=10)
    dut_button.grid(sticky=tk.E + tk.N, row=4, column=3, padx=20, pady=10)

    # new added
    print(path_DUT)
    dut_entry.delete(0, tk.END)
    dut_entry.insert(0, path_DUT)

    confirm_button = tk.Button(root, text="Ok", command=confirm_callback, width=10)
    confirm_button.grid(sticky=tk.E + tk.N, row=5, column=1, padx=20, pady=10)

    cancel_button = tk.Button(root, text="Cancel", command=cancel_callback, width=10)
    cancel_button.grid(sticky=tk.W + tk.N, row=5, column=2, padx=20, pady=10)

    root.mainloop()
    root.destroy()

    # print('g_product_number:' + g_product_number)
    # print('g_tester:' + g_tester)
    return g_product_number, g_tester, req_filename, path_Golden, path_Golden


if __name__ == "__main__":
    mainGUI()

