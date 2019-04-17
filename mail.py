import tkinter as tk
from tkinter import messagebox
import win32com.client as win32
import report
import os
from logger import *

def send_mail():
    """
    This function open outlook.exe.
    send DB check result
    """
    root = tk.Tk()
    root.withdraw()

    var_box = tk.messagebox.askyesno(title='Info', message='Send the result by mail?')

    if var_box:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = 'DB check result'
        mail.Body = "Hi,\nThe DB check result is attached."
        mail.Attachments.Add(report.report_file)
        mail.display()
        logger().info("DB check result has been attached to the mail.")
    else:
        logger().info("Won't send the result by mail.")
    root.destroy()

def send_bug_report():
    """
    send DB check bug report
    """
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = 'DB check bug report'
    mail.Body = "Please describe how you run into this error: "
    mail.To = "shanshan.a.wang@ericsson.com"
    attach = list()
    attach.append(os.getcwd()+log_path()+log_name())
    attach.append(report.g_dut_file)
    attach.append(report.g_golden_file)
    attach.append(report.g_req_file)
    for path in attach:
        if os.path.isfile(path):
            mail.Attachments.Add(path)
    mail.display()
    logger().info("DB check bug report to the mail.")

if __name__ == '__main__':
    send_mail()

