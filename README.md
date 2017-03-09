# reprint [![reprint](https://img.shields.io/pypi/v/reprint.svg)](https://pypi.python.org/pypi/reprint)

reprint is a Python 2/3 module for binding variables and refreshing multi-line output in terminal.

The solution for calculating Unicode char width is from [urwid](https://github.com/urwid/urwid/blob/master/urwid/old_str_util.py)

[中文版README](https://github.com/Yinzo/reprint/blob/master/cn_README.md)


## Features
+ Python 2/3 support
+ Simple variable bindings and automatic command line refresh upon variable change
+ Simultaneous multi-line refresh with each line binded to different variables
+ Robust thread safety with `threading.Lock`

## Setup

```sh
pip install reprint
```

## DEMO

+ [source code](https://github.com/Yinzo/reprint/blob/master/demo/horse_race.py)

![Demo_gif](https://raw.githubusercontent.com/yinzo/reprint/master/demo/images/horse_race_demo.gif)

## Guidance

1. Import the `output` object

	```python
	from reprint import output
	```
2. Use `with` block to control the initialization, `output` object contains the following parameters:
    + `output_type`: `"list"` or `"dict"` (default: `"list"`), indicating the list mode or the dict mode.
    + `initial_len`: `int` (default: `1`), only works in the list mode, indicating the initial length of the list. It's for modifying the content by index without initialization.  
    + `interval`: `int` (default: `0`), the minimal refresh interval (in millisecond). The refresh function call will be ignored unless at least this amount of time has passed since last refresh.

	```python
	with output(output_type="list", initial_len=1, interval=0) as output_list:
	```

3. Changing the variables in `output_list` will trigger the refresh of the command line output.

## Note
+ In the `with` block, any `print`/`logging`/`Exception` commands that print texts on terminal would ruin the format of the reprint output. If you need to append some content to the end of the output, use `append` function in the `output` object (works both in the list or the dict mode).
+ Don't assign a new `list` or `dict` to the `output` object. If you want to change the whole list or dict, use `change` function in the `output` object (works both in the list or the dict mode).
+ Old messages will not be fully wiped out if the height of the output is larger than the height of the terminal window. So you should control the length of your output.
	+ Or you may use the `force_single_line` mode to force the output to stay in single line.

	```python
	with output(output_type="list", initial_len=1, interval=0, force_single_line=True) as output_list:
	```
+ The initialization of threading should be in the `with` block if you use reprint in threading.
+ When used in non-terminal environment, reprint will use the built-in `print` function.
+ Does not work in the IDLE terminal, and any other environment that doesn't provide terminal_size.
+ If you want to disable all warnings, use this:

	```python
	with output(no_warning=True) as output_list:
	```
