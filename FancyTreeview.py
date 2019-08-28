from tkinter import *
from tkinter import ttk


class FancyTreeview(ttk.Treeview):

    def __init__(self, master=None, widths=None, columns=None, **kw):
        self.master = master
        ttk.Treeview.__init__(self, master=master, columns=columns, **kw)

        self._columns = list()
        self.contextMenu = None

        self._setup_header(columns)

        if widths is not None:
            self._set_columns_width(widths)

    def bind_treeviewselect(self, fn):
        """
        Bind action to item select event.
        :param fn: function with arg event=None
        """
        self.bind('<<TreeviewSelect>>', fn)

    def bind_doubleclick(self, fn):
        """
        Bind action to item double clicked event.
        :param fn: function with arg event=None
        """
        self.bind('<Double-Button-1>', fn)

    def setup_context_menu(self, fn_name_list, fn_list):
        """
        Setup right click context menu.
        :param fn_name_list: A list of menu action names. Can be empty.
        :param fn_list: List of functions to add to menu. If no given name, using function name as menu action name.
        """
        if fn_list:
            self.contextMenu = Menu(self, tearoff=0)
            i = 0
            for fn in fn_list:
                try:
                    self.contextMenu.add_command(label=fn_name_list[i], command=fn)
                except IndexError as e:
                    self.contextMenu.add_command(label=fn.__name__, command=fn)
                i = i + 1
            self.bind("<Button-3>", self._popup)

    def set_row_strip(self, flag):
        if flag:
            self.tag_configure('odd', background='#F3F3F3')
        else:
            self.tag_configure('odd', background='#FFFFFF')

    def _set_columns_width(self, widths):
        if len(widths) == len(self._columns):
            for i in range(len(self._columns)):
                self.column(i, width=widths[i])

    def _setup_header(self, headers):
        if headers is not None:
            for header in headers:
                self.heading(header, text=header)
                self._columns.append(header)

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
            if self.get_dec_index(iid) % 2:
                self.set_tag(iid, tags=['odd', ''])
            else:
                self.set_tag(iid, tags=['even', ''])

    def get_dec_index(self, iid):
        # the index is in format like 'I001' and in hex
        return int(iid.lstrip('I'), 16)

    def get_cur_iid(self):
        # select first item if no one is selected
        selection = self.selection()
        if len(selection) > 0:
            return selection[0]
        else:
            self.selection_set("I001")
            return "I001"

    def get_cur_item(self):
        return self.item(self.get_cur_iid())

    def get_next_iid(self):
        next_iid = self.next(self.get_cur_iid())
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