# listprint

listprint 是一个适用于 Python3 的简易变量绑定与多行输出刷新的库

模块内对于 Unicode 字符宽度的计算参考了 [urwid项目](https://github.com/urwid/urwid/blob/master/urwid/old_str_util.py) 内的解决方案

## 特性
+ 简易变量绑定，内容修改时自动刷新命令行输出
+ 多行输出刷新，实现不同行内容由独立变量控制，修改特定变量即能刷新命令行中特定行的内容
+ 多线程安全，使用了 threading.Lock 实现线程安全
+ 无外部库依赖

## DEMO

+ ![源代码](listprint/demo/horse_race.py)
+ ![Demo_gif](listprint/demo/images/horse_race_demo.gif)

## 使用说明
1. `from listprint import output`
2. 使用 Python 的 `with` 语句来进行输出对象的初始化与对象控制，其中 `output` 对象包含以下参数可选：
    1. `output_type`: `"list"` 或 `"dict"`， 分别对应 list 模式与 dict 模式，默认为 `"list"`
    2. `initial_len`: `int`, 只在 list 模式下有效，指定list的初始长度，便于直接使用下标修改而不需初始化, 默认为1
    3. `interval`: `int`, 指定输出的刷新最小间隔，只有两次刷新间隔的毫秒数大于此数才会触发命令行输出刷新。默认为0
3. 修改 `output` 对象内的内容即会刷新

## 注意事项
+ 在 `with` 块内，任何 `print` 、`logging` 或 `Exception` 等其他命令行输出都可能会导致输出格式异常，如果需要追加内容，请使用 `output` 对象的 `append` 函数（list 与 dict 模式都可用）
+ 请勿直接给 `output` 对象赋予 `list` 或 `dict` 等对象，如果需要整体内容替换，请使用 `output` 对象的 `change` 函数（list 与 dict 模式都可用）
+ 当输出内容行数超过当前命令行高度时会导致消息清除不完整。所以若在意输出完成后，命令行的整洁度，请注意控制输出内容的行数。
+ 线程内调用请注意线程的初始化应被包含在 `with` 代码块内




