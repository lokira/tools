from logger import *
from enum import Enum


class CheckEntry(object):
    Y, XY, TABLE = range(3)
    S_IGNORED = "Ignored"
    S_WRONG = "Wrong"
    S_CORRECT = "Correct"
    def __init__(self, title, etype):
        self.title = title
        self.etype = etype
        # In prevent of data not loaded and index out of bound
        self.data = list()
        self.data_G = list()
        if self.etype == self.XY:
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
        self.data_G = data

    def load_data(self, data):
        self.data = data

    def load_t_data(self, data):
        self.t_data = data

    def set_wrong(self):
        self.conclusion = self.S_WRONG

    def set_correct(self):
        self.conclusion = self.S_CORRECT

    def set_ignore(self):
        self.conclusion = self.S_IGNORED

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
        self.comment = comment.strip()

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

    def is_wrong(self):
        return self.conclusion == self.S_WRONG

    def is_ignored(self):
        return self.conclusion == self.S_IGNORED

    def get_title(self):
        return self.title

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

    def to_json(self):
        pass

