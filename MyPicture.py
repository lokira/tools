import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time

label_text = ''
#root = tk.Tk()
#root.withdraw()
new_flag = 0
comments = ''
test_result = 1


def on_click_correct():
    global root
    global comments
    comments = "Correct"
    print("Comments：%s" % comments)
    root.quit()
    return


def on_click_wrong():

    global label_text
    #global root
    global comments
    global test_result
    comments = label_text.get().lstrip()
    if len(comments) == 0:
        messagebox.showwarning(title='Warning', message='Please input comments first!')
        return False

    print("Comments：%s" % comments)
    test_result = 0

    root.quit()
    return


def show_picture(png_file):
    global root
    global new_flag

    #if new_flag != 0:
    root = tk.Tk()
    root.withdraw()


    new_flag = 1

    top = tk.Toplevel()

    top.title('Figure')
    top.resizable(True, True)

    img_open = Image.open(png_file)
    img_png = ImageTk.PhotoImage(img_open)
    label_img = tk.Label(top, image=img_png)
    label_img.pack(side=tk.TOP)

    tk.Label(top, text="If the figure is wong, please input your comments first:", height=2, width=40).pack()

    global label_text
    label_text = tk.StringVar()
    tk.Entry(top, textvariable=label_text, width=60).pack()

    row = tk.Frame(top)
    tk.Button(row, text='correct', command=on_click_correct, width=10).pack(side=tk.LEFT)
    tk.Button(row, text='wrong', command=on_click_wrong, width=10).pack(side=tk.RIGHT)
    row.pack()

    top.mainloop()
    top.destroy()
    return


if __name__ == '__main__':
    show_picture('picture.png')
