# -*- coding: utf8 -*-
import time
from reprint import output

driver_list = ['Alice', 'Bob', 'Eve']
color_list = ["31;1m", "32;1m", "33;1m"]
CSI_list = ["\x1b[", "\033[", "\x1B["]

with output(output_type="dict", interval=0, sort_key=lambda x: int(x[0])) as output:
	for idx, (name, color, CSI) in enumerate(zip(driver_list, color_list, CSI_list)):
		output[str(idx)] = CSI + color + name + CSI + "0m"
