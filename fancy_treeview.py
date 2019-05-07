from tkinter import *
from tkinter import ttk


class FancyTreeview(ttk.Treeview):

    def __init__(self, master=None, widths=None, columns=None, fn_run=None, fn_ignore=None, fn_select=None, **kw):
        self.master = master
        ttk.Treeview.__init__(self, master=master, columns=columns, **kw)

        self._columns = list()
        self.contextMenu = None

        self._setup_header(columns)

        if widths is not None:
            self._set_columns_width(widths)

        self._setup_context_menu(fn_run, fn_ignore)

        self.bind('<<TreeviewSelect>>', fn_select)
        self.bind('<Double-Button-1>', fn_run)

    def _set_columns_width(self, widths):
        if len(widths) == len(self._columns):
            for i in range(len(self._columns)):
                self.column(i, width=widths[i])

    def _setup_header(self, headers):
        if headers is not None:
            for header in headers:
                self.heading(header, text=header)
                self._columns.append(header)

    def _setup_context_menu(self, fn_run, fn_ignore):
        self.contextMenu = Menu(self, tearoff=0)
        self.contextMenu.add_command(label="Run", command=fn_run)
        self.contextMenu.add_command(label="Ignore/Un-ignore", command=fn_ignore)
        self.bind("<Button-3>", self._popup)

    def _popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.selection_set(iid)
            self.focus(iid)
            self.contextMenu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def insert_rows(self, rows):
        for item in rows:
            iid = self.insert('', 'end', values=item)
            # initialize tags as a size 2 array
            if int(iid.lstrip('I'), 16) % 2:
                self.set_tag(iid, tags=['odd', ''])
            else:
                self.set_tag(iid, tags=['even', ''])

    def get_cur_iid(self):
        selection = self.selection()
        return selection[0]

    def get_cur_item(self):
        return self.item(self.get_cur_iid())

    def get_next_iid(self):
        selection = self.selection()
        next_iid = self.next(selection[0])
        return next_iid

    def get_next_item(self):
        if self.get_next_iid() == "":
            # It's already the last row!
            return None
        return self.item(self.get_next_iid())

    def go_next(self):
        iid = self.get_next_iid()
        self.selection_set(iid)
        self.focus(iid)

    def set_tag(self, iid, parity=None, status=None, tags=None):
        item = self.item(iid)
        if tags is not None:
            self.item(iid, tags=tags)
        else:
            tags = item.get("tags")
            if parity is not None:
                tags[0] = parity
            if status is not None:
                tags[1] = status
            self.item(iid, tags=tags)


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500")
    root.mainloop()