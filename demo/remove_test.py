
import time
from reprint import output

with output() as op:
    op.append('Hello')
    op.append("World")
    time.sleep(1)
    op.remove("World")
    time.sleep(1)
    op.remove("Hello")
    time.sleep(1)
    op.append("clean")
