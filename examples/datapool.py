from logger import *
from utilities import open_file
import re
from check_entry import *

class DBEntry(object):

    def __init__(self, cmd, type, data=None):
        self.cmd = cmd
        self.type = type
        if type.startswith("U"):
            def f(v):
                return int(v, 16)
            self.trans = f
        elif type.startswith("S"):
            def f(v):
                return int(v)
            self.trans = f
        elif "char" in type:
            def f(v):
                return v.strip('"').strip()
            self.trans = f
        if data is None:
            self.data = []

    def append(self, d):
        try:
            self.data.append(self.trans(d.strip()))
        except ValueError:
            logger().warning("Incompatible value %s for %s. ", d, self.cmd)

    def trans(self, v):
        return v


class DataPool:

    def __init__(self):
        self.dict_D = dict()
        self.dict_G = dict()

    def init_dict_D(self, path):
        self.read_dict(path, self.dict_D)

    def init_dict_G(self, path):
        self.read_dict(path, self.dict_G)

    def read_dict(self, file_path, dictionary):
        """
        Read commands and data from a file and save them to a dictionary.
        Commands are the keys of the dictionary while data are the values
        of the dictionary.
        Arguments:
            file_path - The file contains all commands and data.
            return - The dictionary of all commands and data.
        """

        f = open_file(file_path)

        wrong_patten = re.compile(r'<|>|Fatal|error|ERROR')
        wrong_flag = 0
        prev_line = ""
        line_no = 0
        cmd = None
        """
        This pattern matches lines in shape of : 
            1. /cmdline P S32
            2. /cmdline S32
            3. /cmdlineS32
        """
        pattern = re.compile(r"(?P<cmd>/\S+)\s*[SPE]{0,2}\s*(?P<type>[S|U]8|[S|U]16|[S|U]32|[S|U]64|char)")
        for line in f:
            line_no += 1
            data = line.strip()
            # Deal with previous deviant lines
            if wrong_flag == 1:
                data = prev_line+data
                logger().warning("Processing line %s with previous line : %s", line_no, data)
                data = re.sub(u"<.*>", "", data)  # This will remove the <> and content in it
                if data == '':
                    logger().warning("No data. Skipped.")
                    continue
                logger().warning("After correction: %s" % data)
                wrong_flag = 0
                prev_line = ""
            # skip useless lines
            if data.startswith('$') or data.startswith('#'):
                continue
            elif wrong_patten.search(data):
                logger().warning("Line %s has wrong patten: %s, process together with next line.", line_no, data)
                wrong_flag = 1
                prev_line = data
                continue

            if data.startswith("/"):
                # data1 = re.split(r"\s+", data)
                m = pattern.match(data)
                if m is not None:
                    cmd = m.group("cmd")
                    entry = DBEntry(cmd, m.group("type"))
                    dictionary[cmd] = entry
                else:
                    logger().warning("String not match to regex pattern! %s" % data)
            else:
                data2 = data.split(",")
                for j in range(len(data2)):
                    temp_data = data2[j].strip()
                    if temp_data != '':
                        if cmd in dictionary:
                            dictionary[cmd].append(temp_data)

    def create_entry_0(self, cmd):
        entry = CheckEntry(cmd, CheckEntry.Y)

        pass

    def create_entry_1(self, cmd):
        pass

    def create_entry_2(self, cmd):
        pass

    def create_entry_3(self, cmd):
        pass

    def create_entry_4(self, cmd):
        pass

    def create_entry_5(self, cmd):
        pass


class CheckEntry:

    def construct(self, dp:DataPool):
        self.get_data(dp)
        self.process_and_validate()

    def get_data(self, dp:DataPool):
        pass

    def process_and_validate(self):
        pass


class OneDimEntry(CheckEntry):

    def get_data(self, dp):
        dp.dict_G.get(self.cmd)
        print("get data 1")

    def process_and_validate(self):
        print("process and validate 2")

class TwoDimEntry(CheckEntry):

    def get_data(self):
        print("get data 2")

    def process_and_validate(self):
        print("process and validate 2")