from logger import *
from enum import Enum

EntryType = Enum('y', ('y', 'xy', 'table'))


class CheckEntry(object):
    def __init__(self, title, etype):
        self.title = title
        self.etype = etype
        # In prevent of data not loaded and index out of bound
        self.data = list()
        self.data_G = list()
        if self.etype == EntryType.xy:
            self.data = list([[], []])
            self.data_G = list([[], []])
        self.t_data = list()
        self.err_msg = list()
        self.legend = list()
        self.xlabel = ""
        self.ylabel = ""
        self.ref = None
        self.conclusion = ""
        self.comment = ""
        self.legend = list()

    def load_data_G(self, data):
        # TODO Deal with legend ？ Or decide while plotting？
        self.data_G = data

    def load_data(self, data):
        self.data = data

    def load_t_data(self, data):
        self.t_data = data

    def set_wrong(self):
        self.conclusion = "Wrong"

    def set_correct(self):
        self.conclusion = "Correct"

    def set_ignore(self):
        self.conclusion = "Ignored"

    def add_err_msg(self, msg):
        self.err_msg.append(msg)

    def set_ref(self, ref):
        if type(ref) in [str, list]:
            self.ref = ref
        else:
            logger().error("Wrong type for CheckEntry ref!")

    def get_ref(self):
        return self.ref

    def set_comment(self, comment):
        self.comment = comment

    def get_comment(self):
        return self.comment

    def get_data(self):
        return self.data

    def get_data_G(self):
        return self.data_G

    def get_t_data(self):
        return self.t_data

    def get_conclusion(self):
        return self.conclusion

    def get_title(self):
        return self.title

    def is_ignored(self):
        return self.conclusion == "Ignored"

    def toggle_ignore(self):
        if self.is_ignored():
            self.conclusion = ""
        else:
            self.set_ignore()

    def get_status_str(self):
        if self.conclusion == "Wrong":
            return "%s : %s - Comment : %s" % (self.title, self.conclusion, self.comment)
        elif self.conclusion == "":
            return self.title
        else:
            return "%s : %s" % (self.title, self.conclusion)

