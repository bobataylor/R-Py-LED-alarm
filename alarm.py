#processes are ending and taking the main process with them
import time


def check_time(HOUR, MIN, TZ):
    now = time.localtime()
    hour = now.tm_hour - TZ
    mint = now.tm_min
    wday = now.tm_wday

    return (hour == HOUR and mint == MIN and wday !=5 and wday !=6)
