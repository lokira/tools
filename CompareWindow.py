import tkinter as tk
from FancyTreeview import *


class CompareWin(tk.Toplevel):
    _width = 500
    _height = 200

    def __init__(self, parent, title, dataset, root=None):
        super().__init__()
        self.title(title)
        self.master = parent
        self.root = root
        if len(dataset) > 0:
            self.tree_frame = Frame(master=self, width=5)
            self.treeview = FancyTreeview(master=self.tree_frame, columns=['golden', 'dut'], show='headings', widths=[250, 250])
            self.treeview.heading('golden', text="Golden")
            self.treeview.heading('dut', text="DUT")
            self.treeview.set_row_strip(True)
            self.treeview.insert_rows(dataset)
            self.treeview.bind('<Control-KeyPress-C>', self.copy)
            self.treeview.bind('<Control-KeyPress-c>', self.copy)
            self.vsb = ttk.Scrollbar(master=self.tree_frame, orient="vertical", command=self.treeview.yview)
            self.treeview.configure(yscrollcommand=self.vsb.set)
            self.treeview.pack(side='left', fill='both', expand='yes')
            self.vsb.pack(side='right', fill='y')
            self.tree_frame.pack(fill='both', expand='yes', padx=(15, 0), pady=(15, 0))
        else:
            label = Label(master=self, text="No difference found in two files.")
            label.pack(padx=4, pady=70)

        bfra = ttk.Frame(self)
        button = Button(master=bfra, text="  Close  ", command=self.destroy)
        button.pack(side='right', padx=10, pady=10)
        bfra.pack(side='bottom', padx=10, fill='both')
        self.center()

    def copy(self, event=None):
        selected = self.treeview.get_cur_item()
        if selected is None:
            return
        cmd = selected['values'][0]
        self.root.clipboard_clear()
        self.root.clipboard_append(cmd)

    def center(self):
        self.update_idletasks()
        if self._width < self.winfo_width():
            self._width = self.winfo_width()
        if self._height < self.winfo_height():
            self._height = self.winfo_height()
        x = int(self.master.winfo_x() + (self.master.winfo_width()-self._width)/2)
        y = int(self.master.winfo_y() + (self.master.winfo_height()-self._height)/2)
        self.geometry("{}x{}+{}+{}".format(self._width, self._height, x, y))
        return x, y

    def show(self):
        self.grab_set()
        self.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x224")
    root.resizable(0, 0)

    def show():
        win = CompareWin(root, "test")
        win.treeview.insert_rows([['aaa','bbb'],['vvv','sss']])
        win.mainloop()

    btn = tk.Button(root, text="OK", command=show)
    btn.pack()

    root.mainloop()