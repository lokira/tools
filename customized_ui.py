import tkinter as tk
import ctypes

set_to_foreground = ctypes.windll.user32.SetForegroundWindow

keybd_event = ctypes.windll.user32.keybd_event
alt_key = 0x12
extended_key = 0x0001
key_up = 0x0002


class PopUp(tk.Toplevel):
    _width = 340
    _height = 100
    _value = False
    entry = None
    default = None

    def __init__(self, parent, title, message, btn, default=None, **kwargs):
        super().__init__()
        self.title(title)
        self.master = parent
        self.resizable(False, False)
        self.default = default
        msg = tk.Label(self, text=message, wraplength=300, justify='left')
        msg.pack(expand=1, fill=tk.BOTH, padx=17, pady=5)
        self.focus_force()
        if kwargs.get("askstring"):
            self.entry = tk.Entry(self)
            self.entry.pack(expand=1, fill=tk.BOTH, padx=25, pady=(3, 7))
            # self.entry.focus_force()
        if "cancel" in btn:
            self.btn2 = tk.Button(self, text="Cancel", command=self.cancel, width=8)
            self.btn2.pack(side=tk.RIGHT, padx=(2, 5), pady=(2, 5))

        if "ok" in btn:
            self.btn1 = tk.Button(self, text="OK", command=self.yes, width=8)
            self.btn1.pack(side=tk.RIGHT, padx=2, pady=(2, 5))

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind('<Return>', self.return_event)
        self.bind('<Escape>', self.escape_event)
        self.center()

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

    def go(self):
        self.wait_visibility()
        self.grab_set()
        if self.entry is not None:
            self.entry.focus_set()
        elif self.default == 'cancel':
            self.btn2.focus_set()
        elif self.default == 'ok':
            self.btn1.focus_set()
        elif self.btn1 is not None:
            self.btn1.focus_set()
        elif self.btn2 is not None:
            self.btn2.focus_set()
        self.mainloop()
        self.destroy()
        return self._value

    def yes(self):
        self.quit()
        if self.entry is not None:
            self._value = self.entry.get()
        else:
            self._value = True

    def cancel(self):
        self.quit()
        if self.entry is not None:
            self._value = ""
        else:
            self._value = False

    def return_event(self, event):
        if self.default is None or self.default == 'cancel':
            self.cancel()
        elif self.default == 'ok':
            self.yes()

    def escape_event(self, event):
        self.cancel()


class Confirm(PopUp):

    def __init__(self, parent=None, title="", message=""):
        super().__init__(parent=parent, title=title, message=message, btn=["ok", "cancel"], default='ok')


class Alert(PopUp):

    def __init__(self, parent=None, title="", message=""):
        super().__init__(parent=parent, title=title, message=message, btn=["ok"], default='ok')


class AskString(PopUp):

    def __init__(self, parent=None, title="", message=""):
        super().__init__(parent=parent, title=title, message=message, btn=["ok", "cancel"], askstring=True, default='ok')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x224")
    root.resizable(0, 0)

    def yes_exit():
        print("do other stuff here then root.destroy")
        root.destroy()

    def exit_root():
        ans = Confirm(parent=root, title="Confirm", message="Leave?").go()
        print("ans is %s"%ans)
        if ans:
            root.quit()

    def clicked():
        ans = AskString(parent=root, title="Hey", message="Please input your comment:Please input your comment:Please input your comment:Please input your comment").go()
        print("ans is %s" % ans)
        if ans == "":
            Alert(parent=root, title="Alert", message="Message is empty!").go()
        print("master focus %s, master next %s, master prev %s."%(
            root.focus_get(),
            root.tk_focusNext(),
            root.tk_focusPrev()))

    btn = tk.Button(root, text="OK", command=clicked)
    btn.pack()

    root.protocol("WM_DELETE_WINDOW", exit_root)
    set_to_foreground(root.winfo_id())
    root.mainloop()
