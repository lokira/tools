import tkinter as tk
from tkinter import messagebox
import re
import win32com.client as win32
import os


class MyMailApp(tk.Toplevel):
    rec_mailbox = ''

    def __init__(self):
        super().__init__()
        self.title('Please input')
        self.setup_ui()

    def setup_ui(self):
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        l1 = tk.Label(row1, text="The receiver mailbox：", height=2, width=40)
        l1.pack(side=tk.TOP)
        self.xls_text = tk.StringVar()
        tk.Entry(row1, textvariable=self.xls_text, width=30).pack(side=tk.BOTTOM)

        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Button(row2, text="OK", command=self.on_click, width=10).pack(side=tk.BOTTOM)

    def on_click(self):
        MyMailApp.rec_mailbox = self.xls_text.get().lstrip()
        if len(MyMailApp.rec_mailbox) == 0:
            messagebox.showwarning(title='Warning', message='please input mailbox!')
            return False

        mailbox_patten = re.compile(r'''(
            ^[a-zA-Z0-9._%+-]+  # username
            @                   # @ symbol
            [a-zA-Z0-9.-]+      # domain name
            \.[a-zA-Z]{2,4}$    #dot-something
            )''', re.VERBOSE)
        if not mailbox_patten.match(MyMailApp.rec_mailbox):
            tk.messagebox.showwarning(title='Warning', message='please input mailbox!')
            return False

        self.quit()
        self.destroy()
        print("Receiver mailbox：%s" % MyMailApp.rec_mailbox)


def send_mail():
    root = tk.Tk()
    root.withdraw()

    var_box = tk.messagebox.askyesno(title='Info', message='Send the result by mail?')

    if var_box:
        #app = MyMailApp()
        #app.mainloop()

        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        """
        receivers = []
        receivers.append(MyMailApp.rec_mailbox)
        mail.To = receivers[0]
        """
        mail.Subject = 'DB check result'
        mail.Body = "Hi,\nThe DB check result is attached."
        mail.Attachments.Add(os.path.abspath('output\\DbCheckReport.docx'))
        # mail.Send()
        mail.display()
        print("DB check result has been sent to %s." % MyMailApp.rec_mailbox)
    else:
        print("Won't send the result by mail.")
    root.destroy()


if __name__ == '__main__':
    send_mail()
