import tkinter as tk
from tkinter import messagebox
import win32com.client as win32
import os


def send_mail():
    root = tk.Tk()
    root.withdraw()

    var_box = tk.messagebox.askyesno(title='Info', message='Send the result by mail?')

    if var_box:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = 'DB check result'
        mail.Body = "Hi,\nThe DB check result is attached."
        mail.Attachments.Add(os.path.abspath('output\\DbCheckReport.docx'))
        mail.display()
        print("DB check result has been sent out.")
    else:
        print("Won't send the result by mail.")
    root.destroy()


if __name__ == '__main__':
    send_mail()
