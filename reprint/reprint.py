# -*- coding: utf-8 -*-
import re
import sys
import time
import shutil
import threading
from math import ceil
from collections import ChainMap

last_output_lines = 0
overflow_flag = False
is_atty = sys.stdout.isatty()

widths = [
    (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
    (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
    (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
    (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
    (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
    (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
    (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]


def get_char_width(char):
    global widths
    o = ord(char)
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


def preprocess(content):
    """
    对输出内容进行预处理，转为str类型，并替换行内\r\t\n等字符为空格
    """

    _content = str(content)
    _content = re.sub(r'\r|\t|\n', ' ', _content)

    return _content


def print_line(content, columns):
    padding = " " * ((columns - line_len(content)) % columns)
    print("{content}{padding}".format(content=content, padding=padding), end='')
    sys.stdout.flush()


def line_len(line):
    """
    计算本行在输出到命令行后所占的宽度
    """
    assert isinstance(line, str)
    result = sum(map(get_char_width, line))
    return result


def lines_of_content(content, border):
    """
    计算内容在特定输出宽度下实际显示的行数
    """
    result = 0
    if isinstance(content, list):
        for line in content:
            _line = preprocess(line)
            result += ceil(line_len(_line) / border)
    elif isinstance(content, dict):
        for k, v in content.items():
            # 加2是算上行内冒号和空格的宽度
            _k, _v = map(preprocess, (k, v))
            result += ceil((line_len(_k) + line_len(_v) + 2) / border)
    return result


def print_multi_line(content):

    global last_output_lines
    global overflow_flag
    global is_atty

    if not is_atty:
        if isinstance(content, list):
            for line in content:
                print(line)
        elif isinstance(content, dict):
            for k, v in sorted(content.items(), key=lambda x: x[0]):
                print("{}: {}".format(k, v))
        else:
            raise TypeError("Excepting types: list, dict. Got: {}".format(type(content)))
        return

    columns, rows = shutil.get_terminal_size()
    lines = lines_of_content(content, columns)
    if lines > rows:
        overflow_flag = True

    # 确保初始输出位置是位于最左处的
    print("\b" * columns, end="")

    if isinstance(content, list):
        for line in content:
            _line = preprocess(line)
            print_line(_line, columns)
    elif isinstance(content, dict):
        for k, v in sorted(content.items(), key=lambda x: x[0]):
            _k, _v = map(preprocess, (k, v))
            print_line("{}: {}".format(_k, _v), columns)
    else:
        raise TypeError("Excepting types: list, dict. Got: {}".format(type(content)))

    # 输出额外的空行来清除上一次输出的剩余内容
    print(" " * columns * (last_output_lines - lines), end="")

    # 回到初始输出位置
    print("\r\b\r" * (max(last_output_lines, lines) + 1), end="")
    sys.stdout.flush()
    last_output_lines = lines


class output:

    class SignalList(list):

        def __init__(self, parent, obj):
            super(output.SignalList, self).__init__(obj)
            self.parent = parent
            self.lock = threading.Lock()

        def change(self, newlist):
            with self.lock:
                self.clear()
                self.extend(newlist)
                self.parent.refresh(int(time.time()), forced=False)

        def __setitem__(self, key, value):
            global is_atty
            with self.lock:
                super(output.SignalList, self).__setitem__(key, value)
                if not is_atty:
                    print("{}".format(value))
                else:
                    self.parent.refresh(int(time.time()), forced=False)

    class SignalDict(dict):

        def __init__(self, parent, obj):
            super(output.SignalDict, self).__init__(obj)
            self.parent = parent
            self.lock = threading.Lock()

        def change(self, newlist):
            with self.lock:
                self.clear()
                super(output.SignalDict, self).__init__(ChainMap(newlist))
                self.parent.refresh(int(time.time()), forced=False)

        def __setitem__(self, key, value):
            global is_atty

            with self.lock:
                super(output.SignalDict, self).__setitem__(key, value)
                if not is_atty:
                    print("{}: {}".format(key, value))
                else:
                    self.parent.refresh(int(time.time()), forced=False)

    def __init__(self, output_type="list", initial_len=1, interval=0):

        if output_type is "list":
            self.warped_obj = output.SignalList(self, [''] * initial_len)
        elif output_type is "dict":
            self.warped_obj = output.SignalDict(self, {})

        self.interval = interval
        self._last_update = int(time.time())

    def refresh(self, new_time=0, forced=True):
        if new_time - self._last_update > self.interval or forced:
            print_multi_line(self.warped_obj)
            self._last_update = new_time

    def __enter__(self):
        global is_atty
        if not is_atty:
            print("Not in terminal, reprint now using normal build-in print function.")

        return self.warped_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        global is_atty

        self.refresh(forced=True)
        if is_atty:
            columns, _ = shutil.get_terminal_size()
            print('\n' * lines_of_content(self.warped_obj, columns), end="")
            global last_output_lines
            global overflow_flag
            last_output_lines = 0
            if overflow_flag:
                print("Detected that the lines of output has been exceeded the height of terminal windows, which \
                caused the former output remained and keep adding new lines.")
                print("检测到输出过程中, 输出行数曾大于命令行窗口行数, 这会导致输出清除不完整, 而使输出不停增长。请注意控制输出行数。")
