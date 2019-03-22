"""
This module includes functions about plotting and figure display.
"""
import matplotlib.pyplot as plt
from tkinter import simpledialog
from tkinter import messagebox
import report
from logger import *

import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

root = None


def on_fig_closed():
    """
    Called when quit button clicked.
    """
    var_box = messagebox.askyesno(title='Info', message='Are you sure to quit?')
    if var_box:
        logger().warning("Execution abort due to user operation!")
        exit(0)


def plot_fmt_G(*data, style='unknown'):
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

    plt.plot(*data, color='#FB7D07', marker=m_marker,
             markersize=6, linestyle=m_style, alpha=0.7, linewidth=1)


def plot_fmt(*data, style='unknown'):
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
    plt.plot(*data, color='#0652FF', marker=m_marker,
             markersize=4, linestyle=m_style, linewidth=1)


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
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    button = tkinter.Button(master=root, text="Wrong", command=on_click_func("Wrong", title))
    button.pack(side=tkinter.RIGHT)
    button = tkinter.Button(master=root, text="Correct", command=on_click_func("Correct", title))
    button.pack(side=tkinter.RIGHT)

    root.protocol("WM_DELETE_WINDOW", on_fig_closed)

    tkinter.mainloop()
    # clear previous figure
    plt.clf()
    plt.cla()


def on_click_func(btn, cmd):
    """
    Generate callback functions for OK/NOK buttons on the figure.
    """
    global root
    if btn == "Correct":
        def func():
            comments = "Correct"
            report.save_figure(cmd, comments)
            root.quit()
            root.destroy()
    else:
        def func():
            m_comment = simpledialog.askstring("Comment Required", "Please input your comment:")
            if m_comment and m_comment.strip():
                comments = m_comment
                report.save_figure(cmd, comments)
                root.quit()
                root.destroy()
                logger().debug("NOK graph comment: %s", m_comment)
            else:
                messagebox.showwarning(title='Warning', message='Please input comments first!')

    return func


if __name__ == '__main__':
    show_picture('picture.png')
