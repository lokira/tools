"""
This module includes functions about plotting and figure display.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import simpledialog
from tkinter import messagebox
import report


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
    plt.subplots_adjust(bottom=0.15)
    b_ok = Button(plt.axes([0.7, 0.01, 0.1, 0.05]), 'Correct')
    b_nok = Button(plt.axes([0.82, 0.01, 0.1, 0.05]), 'Wrong')
    b_ok.on_clicked(on_click_func("Correct", title))
    b_nok.on_clicked(on_click_func("Wrong", title))

    plt.show()

    # clear previous figure
    plt.clf()
    plt.cla()


def on_click_func(btn, cmd):
    """
    Generate callback functions for OK/NOK buttons on the figure.
    """
    if btn == "Correct":
        def func(event):
            comments = "Correct"
            report.save_figure(cmd, comments)
    else:
        def func(event):
            m_comment = simpledialog.askstring("Comment Requied", "Please input your comment:")
            if m_comment and m_comment.strip():
                comments = m_comment
                report.save_figure(cmd, comments)
                print(m_comment)
            else:
                messagebox.showwarning(title='Warning', message='Please input comments first!')

    return func


if __name__ == '__main__':
    show_picture('picture.png')
