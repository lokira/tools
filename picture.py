"""
This module includes functions about plotting and figure display.
"""
import matplotlib.pyplot as plt
from check_entry import *
import report
from logger import *
from sys import exit
import utilities as uti
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from customized_ui import *
from fancy_treeview import *

root = None
winfo_x, winfo_y = 10, 10
comment_flag = False

DUT_S = "DUT"
GOLDEN_S = "Golden"


class SimpleTable(tkinter.Frame):
    def __init__(self, parent, rows=2, columns=2, data=None):
        # use black background so it "peeks through" to
        # form grid lines
        tkinter.Frame.__init__(self, parent, background="grey")
        self._widgets = []

        if data is None:
            data = [[""]*columns for i in range(rows)]

        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tkinter.Label(self, text=data[row][column], borderwidth=0, width=20)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


class StatusBar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, anchor=W)  # relief=SUNKEN
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class CheckWindow(ttk.Frame):
    """
    Main window of check.
    """
    def __init__(self, entry_list, master=None, **kw):
        ttk.Frame.__init__(self, master=master, **kw)
        self.master = master
        self.entry_list = entry_list
        self._init_tree()
        for i, entry in enumerate(self.entry_list):
            self.tree.insert_rows([[entry.title, entry.conclusion, i]])
        self.center = tk.Canvas(master=self)
        self.sbar = StatusBar(self)
        self._init_toolbar()
        # Pack widgets
        self.toolbar.pack(side='top', fill='x')
        self.sbar.pack(side='bottom', fill='x')
        self.tree_frame.pack(side='left', fill='y')
        self.center.pack(side='right', fill='both', expand='yes')
        self.update_color()
        self.master.protocol("WM_DELETE_WINDOW", self._on_closed)

    def _init_tree(self):
        """
        Create a fancy tree view
        """
        self.tree_frame = Frame(master=self, width=5)
        self.tree = FancyTreeview(master=self.tree_frame,
                                  columns=['Item', 'Conclusion'],
                                  show='headings',
                                  widths=[200, 40],
                                  fn_run=self.fn_run,
                                  fn_ignore=self.fn_toggle_ignore,
                                  fn_select=self.fn_select)
        self.vsb = ttk.Scrollbar(master=self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.tree.pack(side='left', fill='both', expand='yes')
        self.vsb.pack(side='right', fill='y')

    def _init_toolbar(self):
        self.toolbar = Frame(self)
        self.img = PhotoImage(file='./download1.png')
        self.btn_gen_rep = Button(self.toolbar, compound='left', image=self.img, text="Generate\nReport", command=self.fn_generate_report)
        self.btn_gen_rep.pack(side='left', padx=4, pady=2)

    def set_center(self, center_widget):
        """
        Set center widget of this window
        """
        self.center.destroy()
        self.center = center_widget
        self.center.pack(side='left', fill='both', expand='yes')

    def fn_run(self, event=None):
        """
        Function for run action of tree view context menu.
        """
        entry = self.get_entry(self.tree.get_cur_item())
        print(entry.get_data())
        print(entry.get_data_G())
        print(entry.err_msg)
        self.show_plot(entry)

    def fn_toggle_ignore(self, event=None):
        """
        Function for ignore action of tree view context menu.
        """
        entry = self.get_entry(self.tree.get_cur_item())
        entry.toggle_ignore()
        entry.set_comment("")
        if entry.is_ignored():
            self.set_conclusion(self.tree.get_cur_iid(), 'Ignored')
            self.tree.set_tag(self.tree.get_cur_iid(), status='ignored')
        else:
            self.set_conclusion(self.tree.get_cur_iid(), '')
            self.tree.set_tag(self.tree.get_cur_iid(), status='')
        self.update_color()
        if entry.is_ignored():  # If un-ignore is applied, we stay at current entry
            next_item = self.tree.get_next_item()
            if next_item:
                next_entry = self.get_entry(next_item)
                self.tree.go_next()
                self.show_plot(next_entry)
        # Update status bar.
        self.fn_select()

    def fn_select(self, event=None):
        """
        Event handler for select event of tree view.
        """
        entry = self.get_entry(self.tree.get_cur_item())
        self.sbar.set(entry.get_status_str())

    def fn_generate_report(self):
        # TODO Check data before generate.
        result = "PASSED"
        for entry in self.entry_list:
            if entry.get_conclusion() is "":
                Alert(parent=self.master, title='DB Check',
                      message='Please check all the entries or set to ignored before generating report!').go()
                return
            if entry.is_wrong():
                result = "NOT PASSED"
        report.generate_test_report(self.entry_list, result)

    def load_tree(self, rows):
        self.tree.insert_rows(rows)

    def set_conclusion(self, iid, res):
        """
        Set conclusion column for a row in the tree view.
        """
        self.tree.set(iid, column="#2", value=res)

    def correct(self, event=None):
        cur_item = self.tree.get_cur_item()
        cur_entry = self.get_entry(cur_item)
        cur_entry.set_correct()
        cur_entry.set_comment("Correct")
        if cur_entry.etype == EntryType.table:
            cur_entry.set_ref(cur_entry.get_t_data())
        else:
            path = report.save_figure(cur_entry.title)
            cur_entry.set_ref(path)
        self.set_conclusion(self.tree.get_cur_iid(), "OK")
        self.tree.set_tag(self.tree.get_cur_iid(), status='correct')
        self.update_color()
        # Move on to next item
        next_item = self.tree.get_next_item()
        if next_item:
            next_entry = self.get_entry(next_item)
            self.tree.go_next()
            self.show_plot(next_entry)

    def wrong(self, event=None):
        cur_item = self.tree.get_cur_item()
        cur_entry = self.get_entry(cur_item)
        cur_entry.set_wrong()
        m_comment = AskString(parent=self.master, title="Comment Required", message="Please input your comment:").go()
        if m_comment and m_comment.strip():
            if cur_entry.etype == EntryType.table:
                cur_entry.set_ref(cur_entry.get_t_data())
            else:
                path = report.save_figure(cur_entry.title)
                cur_entry.set_ref(path)
            logger().debug("NOK graph comment: %s", m_comment)
            cur_entry.set_comment(m_comment)
            self.set_conclusion(self.tree.get_cur_iid(), "NG")
            # self.tree.set_tag(self.tree.get_cur_iid(), 'wrong')
            self.tree.set_tag(self.tree.get_cur_iid(), status='wrong')
            self.update_color()
            # Move on to next item
            next_item = self.tree.get_next_item()
            if next_item:
                next_entry = self.get_entry(next_item)
                self.tree.go_next()
                self.show_plot(next_entry)
        else:
            Alert(parent=self.master, title='Warning', message='Please input comments first!').go()

    def show_plot(self, entry):
        fra = ttk.Frame(self)
        """
        # ===Draw buttons===
        """
        bfra = ttk.Frame(fra)
        button = tkinter.Button(master=bfra, text="Wrong", command=self.wrong)
        button.pack(side=tkinter.RIGHT, padx=5)
        self.master.bind('x', self.wrong)
        button = tkinter.Button(master=bfra, text="Correct", command=self.correct)
        button.pack(side=tkinter.RIGHT, padx=5)
        self.master.bind('c', self.correct)
        bfra.pack(side='bottom', fill='both')
        """
        # ===Draw Plot/Table===
        """
        if entry.etype == EntryType.table:
            t = SimpleTable(fra, rows=len(entry.get_t_data()), columns=3, data=entry.get_t_data())
            t.pack(side="top", fill="both")
        else:
            plt.clf()
            plt.cla()
            if entry.etype == EntryType.xy:
                plot_fmt_G(entry.get_data_G()[0], entry.get_data_G()[1], cmd=entry.title, xlabel=entry.xlabel, ylabel=entry.ylabel)
                plot_fmt(entry.get_data()[0], entry.get_data()[1], cmd=entry.title, xlabel=entry.xlabel, ylabel=entry.ylabel)
                plt.legend(["Golden", "DUT"])
            elif entry.etype == EntryType.y:
                plot_fmt_G(entry.get_data_G(), cmd=entry.title, xlabel=entry.xlabel, ylabel=entry.ylabel)
                plot_fmt(entry.get_data(), cmd=entry.title, xlabel=entry.xlabel, ylabel=entry.ylabel)
                plt.legend(["Golden", "DUT"])
            plt.xticks(rotation=30)
            fig = plt.gcf()
            canvas = FigureCanvasTkAgg(fig, master=fra)  # A tk.DrawingArea.
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, fra)
            toolbar.update()
            canvas.get_tk_widget().pack(side='top', fill='both', expand='yes')

        self.set_center(fra)
        """
        # ===Show errors===
        """
        if len(entry.err_msg):
            Alert(parent=self.master, title="DB Check", message=str.join('\n', entry.err_msg)).go()
            logger().error(str.join('\n', entry.err_msg))

    def get_entry(self, item):
        index = item.get("values")[2]
        return self.entry_list[index]

    def update_color(self):
        self.tree.tag_configure('wrong', foreground='red')
        self.tree.tag_configure('ignored', foreground='gray60')
        self.tree.tag_configure('odd', background='#F3F3F3')

    def _on_closed(self):
        """
        Called when quit button clicked.
        """
        var_box = Confirm(parent=self.master, title='Info', message='Are you sure to quit?').go()
        if var_box:
            logger().warning("Execution abort due to user operation!")
            exit(0)


def plot_fmt_G(*data, style='unknown', cmd, xlabel="", ylabel=""):
    """
    Draw golden data with its style.
    Arguments:
        data - Datasets to be plot. Accept 1 or 2 arrays as y or x, y.
        style - Set the marker and line style.
    """
    if style == 'p':
        m_marker = '*'
        m_style = ''
    elif style == 'l':
        m_marker = ''
        m_style = ':'
    else:
        m_marker = '*'
        m_style = ':'
    try:
        plt.plot(*data, color='#FB7D07', marker=m_marker,
                 markersize=6, linestyle=m_style, alpha=0.7, linewidth=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(cmd)
        return True
    except ValueError as e:
        if uti.is_substring("x and y must have same first dimension", e.args[0]):
            logger().exception("The number of x and y values are not match! cmd: %s", cmd)
        else:
            logger().exception("Failed to plot %s golden. There might be a format error in the golden file.", cmd)
        return False


def plot_fmt(*data, style='unknown', cmd='unknown', xlabel="", ylabel=""):
    """
    Draw dut data with its style.
    Arguments:
        data - Datasets to be plot. Accept 1 or 2 arrays as y or x, y.
        style - Set the marker and line style.
    """
    if style == 'p':
        m_marker = '.'
        m_style = ''
    elif style == 'l':
        m_marker = ''
        m_style = '-'
    else:
        m_marker = '.'
        m_style = '-'
    try:
        plt.plot(*data, color='#0652FF', marker=m_marker,
                 markersize=4, linestyle=m_style, linewidth=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(cmd)
        return True
    except ValueError as e :
        if uti.is_substring("x and y must have same first dimension", e.args[0]):
            logger().exception("The number of x and y values are not match! cmd: %s", cmd)
        else:
            logger().exception("Failed to plot %s. There might be a format error in the dut db file.", cmd)
        return False


def open_check_win(check_entry_list):
    root = Tk()
    root.geometry("820x610+10+10")
    mainframe = CheckWindow(check_entry_list, master=root)
    mainframe.pack(side='top', fill='both', expand='yes')
    root.mainloop()
