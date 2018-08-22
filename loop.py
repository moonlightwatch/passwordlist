# coding=utf-8

import os
import time

interval_hours = 3
interval_minutes = 0
interval_seconds = 0


def do_something():
    os.popen("python3 update.py", "w", 1)


mark_time = time.time()

interval_seconds += interval_hours*60*60 + interval_minutes*60

while True:
    seconds = time.time()-mark_time
    if seconds > interval_seconds:
        do_something()
        mark_time = time.time()
    time.sleep(interval_seconds/2)

