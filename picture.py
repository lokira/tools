"""
This module includes functions about plotting and figure display.
"""
import matplotlib.pyplot as plt
from tkinter import simpledialog
from tkinter import messagebox
import report
from logger import *
from sys import exit
import utilities as uti
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

root = None
winfo_x, winfo_y = 10, 10
comment_flag = False


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


def on_fig_closed():
    """
    Called when quit button clicked.
    """
    var_box = messagebox.askyesno(title='Info', message='Are you sure to quit?')
    if var_box:
        logger().warning("Execution abort due to user operation!")
        exit(0)


def plot_fmt_G(*data, style='unknown', cmd):
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
    except ValueError as e:
        if uti.is_substring("x and y must have same first dimension", e.args[0]):
            logger().exception("The number of x and y values are not match! cmd: %s", cmd)
            messagebox.showwarning(title="DB Check",
                                   message="Failed to plot %s golden!\nThe number of x and y values are not match!" % cmd)
        else:
            logger().exception("Failed to plot %s golden. There might be a format error in the golden file.", cmd)
            messagebox.showwarning(title="DB Check",
                                   message="Failed to plot %s golden!\nThere might be a format error in your golden file!"%cmd)


def plot_fmt(*data, style='unknown', cmd='unknown'):
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
    except ValueError as e :
        if uti.is_substring("x and y must have same first dimension", e.args[0]):
            logger().exception("The number of x and y values are not match! cmd: %s", cmd)
            messagebox.showwarning(title="DB Check",
                                   message="Failed to plot %s dut!\nThe number of x and y values are not match!" % cmd)
        else:
            logger().exception("Failed to plot %s. There might be a format error in the dut db file.", cmd)
            messagebox.showwarning(title="DB Check",
                                   message="Failed to plot %s dut!\nThere might be a format error in your dut data file!"%cmd)


def save_size(event):
    global winfo_x, winfo_y
    winfo_x, winfo_y = root.winfo_x(), root.winfo_y()


def plot_show(title, legend=['golden', 'dut'], xlabel=None, ylabel=None, **kwargs):
    """
    Open a interactive window to display the figure.
    Arguments:
        title - Text to display as the title.
        legend - Legends for different datasets.
        xlabel - Text to display as xlabel.
        ylabel - Text to display as ylabel.
    """
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(legend)
    plt.title(title)
    # Show the figure in a tk window
    global root
    fig = plt.gcf()
    root = tkinter.Tk()
    root.wm_title(title)
    root.geometry("+%d+%d" % (winfo_x, winfo_y))
    root.bind("<Configure>", save_size)
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    button = tkinter.Button(master=root, text="Wrong", command=on_click_func("Wrong", title))
    button.pack(side=tkinter.RIGHT, padx=5)
    root.bind('x', on_click_func("Wrong", title))
    button = tkinter.Button(master=root, text="Correct", command=on_click_func("Correct", title))
    button.pack(side=tkinter.RIGHT, padx=5)
    root.bind('c', on_click_func("Correct", title))

    root.protocol("WM_DELETE_WINDOW", on_fig_closed)
    root.focus_force()
    if kwargs["gd_no_match"]:
        messagebox.showwarning("DB Check", "The number of values is different between Golden and DUT data!")

    tkinter.mainloop()
    # clear previous figure
    plt.clf()
    plt.cla()


def on_click_func(btn, cmd, t_data=None):
    """
    Generate callback functions for OK/NOK buttons on the figure.
    """
    global root
    if btn == "Correct":
        def func(e=None):
            global comment_flag
            if comment_flag:
                return
            comments = "Correct"
            if t_data is not None:
                report.save_tdata(cmd, comments, t_data)
            else:
                report.save_figure(cmd, comments)
            root.quit()
            root.destroy()
    else:
        def func(e=None):
            global comment_flag
            if comment_flag:
                return
            comment_flag = True
            m_comment = simpledialog.askstring("Comment Required", "Please input your comment:", parent=root)
            if m_comment and m_comment.strip():
                comments = m_comment
                if t_data is not None:
                    report.save_tdata(cmd, comments, t_data)
                else:
                    report.save_figure(cmd, comments)
                root.quit()
                root.destroy()
                logger().debug("NOK graph comment: %s", m_comment)
            else:
                messagebox.showwarning(title='Warning', message='Please input comments first!')
                root.focus_force()
            comment_flag = False
    return func


def table_show(title, data):
    global root
    root = tkinter.Tk()
    root.wm_title(title)
    root.geometry("+%d+%d" % (winfo_x, winfo_y))
    root.bind("<Configure>", save_size)

    t = SimpleTable(root, rows=len(data), columns=3, data=data)
    t.pack(side="top", fill="x")

    button = tkinter.Button(master=root, text="Wrong", command=on_click_func("Wrong", title, t_data=data))
    button.pack(side=tkinter.RIGHT, padx=5)
    root.bind('x', on_click_func("Wrong", title, t_data=data))
    button = tkinter.Button(master=root, text="Correct", command=on_click_func("Correct", title, t_data=data))
    button.pack(side=tkinter.RIGHT, padx=5)
    root.bind('c', on_click_func("Correct", title, t_data=data))

    root.protocol("WM_DELETE_WINDOW", on_fig_closed)
    root.focus_force()
    tkinter.mainloop()


if __name__ == '__main__':
    show_picture('picture.png')
