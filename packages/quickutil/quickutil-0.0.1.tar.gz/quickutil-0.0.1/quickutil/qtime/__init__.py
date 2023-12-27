import time

def wait(milliseconds = 10):
    time.sleep(milliseconds / 1000)

def epoch():
    return time.time()

def date(format = "%a %b %d %H:%M:%S %Y"):
    return time.strftime(format)

def runtime():
    return time.perf_counter()