"""
This module includes methods for displaying main GUI.
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import init_parameter as ini
import report
from sys import exit
import os
from logger import *

root = tk.Tk()

req_entry = tk.Entry(root, width=40)
golden_entry = tk.Entry(root, width=40)
dut_entry = tk.Entry(root, width=40)
output_entry = tk.Entry(root, width=40)

product_number = ''
tester = ''
s_req_file = ''
s_golden_file = ''
s_dut_file = ''
s_output_dir = ''

req_filename = ''
path_Golden = ''
path_DUT = ''
output_dir = ''


def req_callback():
    """
    Open requirements file select window.
    """
    global req_entry
    global req_filename

    req_filename = filedialog.askopenfilename(title='select the DB requirement file',
                                              filetypes=[('text file', '*.txt'), ('All Files', '*')])
    logger().debug("Requirement file selected: %s", req_filename)
    req_entry.delete(0, tk.END)
    req_entry.insert(0, req_filename)


def golden_callback():
    """
    Open golden file select window.
    """
    global golden_entry
    global path_Golden
    path_Golden = filedialog.askopenfilename(title='select the old golden DB file',
                                             filetypes=[('text file', '*.txt'), ('All Files', '*')])
    logger().debug("Golden file selected: %s", path_Golden)
    golden_entry.delete(0, tk.END)
    golden_entry.insert(0, path_Golden)


def dut_callback():
    """
    Open dut data file select window.
    """
    global dut_entry
    global path_DUT

    path_DUT = filedialog.askopenfilename(title='select the new DUT DB file',
                                          filetypes=[('text file', '*.txt'), ('All Files', '*')])
    logger().debug("DUT data file selected: %s", path_DUT)
    dut_entry.delete(0, tk.END)
    dut_entry.insert(0, path_DUT)


def output_callback():
    """
    Open output path selection window.
    """
    global output_entry
    global output_dir

    output_dir = filedialog.askdirectory(title='select the output directory')
    logger().debug("Output path selected: %s", output_dir)
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)


def confirm_callback():
    """
    Check and save parameters. Confirm to continue working.
    """
    global root
    global product_number
    global tester
    global s_req_file
    global s_golden_file
    global s_dut_file
    global s_output_dir
    global req_filename
    global path_Golden
    global path_DUT
    global output_dir

    g_product_number = product_number.get().lstrip()
    if len(g_product_number) == 0:
        messagebox.showwarning(title='Warning', message='Please input product number!')
        return False

    g_tester = tester.get().lstrip()
    if len(g_tester) == 0:
        messagebox.showwarning(title='Warning', message='Please input tester!')
        return False

    g_req_file = s_req_file.get().lstrip()
    if len(g_req_file) == 0:
        messagebox.showwarning(title='Warning', message='Please select requirement file!')
        return False
    else:
        req_filename = g_req_file

    g_golden_file = s_golden_file.get().lstrip()
    if len(g_golden_file) == 0:
        messagebox.showwarning(title='Warning', message='Please select golden file!')
        return False
    else:
        path_Golden = g_golden_file

    g_dut_file = s_dut_file.get().lstrip()
    if len(g_dut_file) == 0:
        messagebox.showwarning(title='Warning', message='Please select dut file!')
        return False
    else:
        path_DUT = g_dut_file

    g_output_dir = s_output_dir.get().lstrip()
    if not g_output_dir:
        output_dir = os.path.join(os.getcwd(), 'output')
    else:
        output_dir = g_output_dir

    ini.save_last_parameters('lastDBCheckPara.txt', g_product_number, g_tester, req_filename, path_Golden, path_DUT, output_dir)
    report.store_parameter(g_product_number, g_tester, req_filename, path_Golden, path_DUT, output_dir)
    root.quit()

    return


def cancel_callback():
    """
    Exit the program.
    """
    global root
    root.quit()
    exit(0)


def on_closing():
    """
    Called when the quit button on the top of the window is pushed.
    """
    root.destroy()
    exit(0)


def mainGUI(version):
    """
    Method to show the main GUI.
    Arguments:
        version - version of db_check.exe
    """

    global root
    global product_number
    global tester
    global req_filename
    global path_Golden
    global path_DUT
    global s_req_file
    global s_golden_file
    global s_dut_file
    global s_output_dir

    root.title("DBCheck - version " + version)
    try:
        last_product_number, last_tester, req_filename, path_Golden, path_DUT, output_dir = \
            ini.read_last_parameters('lastDBCheckPara.txt')
    except ValueError as e:
        logger().warning("Failed to read last parameters.")
        last_product_number, last_tester, req_filename, path_Golden, path_DUT, output_dir = [""]*6

    product_number_label = tk.Label(root, text="Product Number:")
    product_number_label.grid(sticky=tk.E, row=0, column=0, columnspan=1, padx=20, pady=10)

    product_number = tk.StringVar()
    product_number_entry = tk.Entry(root, textvariable=product_number, width=30)
    product_number_entry.grid(sticky=tk.W, row=0, column=1, columnspan=2, padx=20, pady=10)

    logger().debug("last product number: %s", last_product_number)
    product_number_entry.delete(0, tk.END)
    product_number_entry.insert(0, last_product_number)

    tester_label = tk.Label(root, text="Tester:")
    tester_label.grid(sticky=tk.E, row=1, column=0, columnspan=1, padx=20, pady=10)

    tester = tk.StringVar()
    tester_entry = tk.Entry(root, textvariable=tester, width=30)
    tester_entry.grid(sticky=tk.W, row=1, column=1, columnspan=2, padx=20, pady=10)

    logger().debug("last tester: %s", last_tester)
    tester_entry.delete(0, tk.END)
    tester_entry.insert(0, last_tester)

    req_label = tk.Label(root, text="DB requirement file:")
    req_label.grid(sticky=tk.E, row=2, column=0, columnspan=1, padx=20, pady=10)

    s_req_file = tk.StringVar()
    global req_entry
    req_entry = tk.Entry(root, textvariable=s_req_file, width=80)
    req_entry.grid(row=2, column=1, columnspan=2, padx=20, pady=10)
    req_button = tk.Button(root, text="select", command=req_callback, width=10)
    req_button.grid(sticky=tk.E + tk.N, row=2, column=3, padx=20, pady=10)

    logger().debug("last requirement : %s", req_filename)
    req_entry.delete(0, tk.END)
    req_entry.insert(0, req_filename)

    golden_label = tk.Label(root, text="Golden DB file:")
    golden_label.grid(sticky=tk.E, row=3, column=0, columnspan=1, padx=20, pady=10)

    s_golden_file = tk.StringVar()
    global golden_entry
    golden_entry = tk.Entry(root, textvariable=s_golden_file, width=80)
    golden_entry.grid(row=3, column=1, columnspan=2, padx=20, pady=10)
    golden_button = tk.Button(root, text="select", command=golden_callback, width=10)
    golden_button.grid(sticky=tk.E + tk.N, row=3, column=3, padx=20, pady=10)

    logger().debug("last golden file : %s", path_Golden)
    golden_entry.delete(0, tk.END)
    golden_entry.insert(0, path_Golden)

    dut_label = tk.Label(root, text="DUT DB file:")
    dut_label.grid(sticky=tk.E, row=4, column=0, columnspan=1, padx=20, pady=10)

    s_dut_file = tk.StringVar()
    global dut_entry
    dut_entry = tk.Entry(root, textvariable=s_dut_file, width=80)
    dut_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=10)
    dut_button = tk.Button(root, text="select", command=dut_callback, width=10)
    dut_button.grid(sticky=tk.E + tk.N, row=4, column=3, padx=20, pady=10)

    logger().debug("last DUT file : %s", path_DUT)
    dut_entry.delete(0, tk.END)
    dut_entry.insert(0, path_DUT)

    output_label = tk.Label(root, text="Output directory:")
    output_label.grid(sticky=tk.E, row=5, column=0, columnspan=1, padx=20, pady=10)

    s_output_dir = tk.StringVar()
    global output_entry
    output_entry = tk.Entry(root, textvariable=s_output_dir, width=80)
    output_entry.grid(row=5, column=1, columnspan=2, padx=20, pady=10)
    output_button = tk.Button(root, text="select", command=output_callback, width=10)
    output_button.grid(sticky=tk.E + tk.N, row=5, column=3, padx=20, pady=10)

    logger().debug("last output directoryff : %s", output_dir)
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

    confirm_button = tk.Button(root, text="Ok", command=confirm_callback, width=10)
    confirm_button.grid(sticky=tk.E + tk.N, row=6, column=1, padx=20, pady=10)

    cancel_button = tk.Button(root, text="Cancel", command=cancel_callback, width=10)
    cancel_button.grid(sticky=tk.W + tk.N, row=6, column=2, padx=20, pady=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
    root.destroy()
    return req_filename, path_Golden, path_DUT


if __name__ == "__main__":
    mainGUI()

