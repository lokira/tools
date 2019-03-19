import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import simpledialog
from tkinter import messagebox
import report

label_text = ''
#root = tk.Tk()
#root.withdraw()
new_flag = 0


def plot_fmt_G(*data, style='unknown'):
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
    if btn == "Correct":
        def func(event):
            comments = "Correct"
            report.save_output(cmd, comments)
    else:
        def func(event):
            m_comment = simpledialog.askstring("Comment Requied", "Please input your comment:")
            if m_comment and m_comment.strip():
                comments = m_comment
                report.save_output(cmd, comments)
                print(m_comment)
            else:
                messagebox.showwarning(title='Warning', message='Please input comments first!')

    return func


if __name__ == '__main__':
    show_picture('picture.png')
