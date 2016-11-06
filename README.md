# reprint [![reprint](https://img.shields.io/pypi/v/reprint.svg)](https://pypi.python.org/pypi/reprint)

reprint is a module for Python 2/3 to binding variables and refresh multi line output in terminal.

The solution for calculating Unicode char width is from [urwid](https://github.com/urwid/urwid/blob/master/urwid/old_str_util.py) 

[中文版README](https://github.com/Yinzo/reprint/blob/master/cn_README.md)


## Feature
+ Support Python 2/3
+ variables binding, automatically refresh command line output when variables changed
+ multi line contents flush-able, every line of output comes from different variable in output object, changes on variable will refresh output
+ thread safe, using threading.Lock to do that

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
2. Use `with` block to control the initalization ，`output` object contain these following parameters:
    + `output_type`: `"list"` or `"dict"`， indicating list mode and dict mode, default as `"list"`
    + `initial_len`: `int`, only work in list mode, indicating the initial length of the list, for do some modification on the content without initialization, default as `1`
    + `interval`: `int`, the interval of refresh，only greater than this interval will trigger the refresh function, default as `0`

	```python
	with output(output_type="list", initial_len=1, interval=0) as output_list:
	```

3. Change the variables in `output_list` will trigger the refresh of the command line output

## Note
+ Within `with` block, any `print`/`logging`/`Exception` that do output on terminal would cause the format of reprint output abnormal. If you need to append some content to the end of output, use `append` function of `output` instance (works both in list or dict mode)
+ Don't assign a new `list` or `dict` to `output` instance. If you want to entirely change the list or dict, use `change` function of `output` instance (works both in list or dict mode)
+ If the lines of output exceed the height of terminal windows, that will cause the former output remained and keep adding new lines to the terminal. So maybe you should control the length of your `output` instance
+ The initialzation of threading should be within the `with` block if you use reprint in threading
+ When using non-terminal output, reprint will use normal build-in `print` function.

