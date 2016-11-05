import time
import random
import threading

from reprint import output


def some_op(index=0):
    LENGTH = 100
    global output_list
    now = 0
    while now < LENGTH:
        max_step = LENGTH-now
        step = random.randint(1, max_step or 1)
        now += step

        output_list[index] = "{}{}{padding}{ending}".format(
            "-" * now,
            index,
            padding=" " * (LENGTH-now-1) if now < LENGTH else "",
            ending="|" if now < LENGTH else ""
        )

        time.sleep(1)

    output_list.append("{} finished".format(index))

with output(output_type="list", initial_len=5, interval=0) as output_list:
    pool = []
    for i in range(5):
        t = threading.Thread(target=some_op, args=(i,))
        t.start()
        pool.append(t)
    [t.join() for t in pool]
