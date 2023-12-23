#from . import loggerjava
import time
if __name__ == '__main__':
    pass
"""
class loggerjava():

    def __init__(self):
        name = "log"
        f = open(name+".log", "w")
        f.close()
        showdetailedtime = False
        showinconsole = True

    def debug( txt, pos="main"):
        level = 'debug'
        f = open(name + ".log", "at+")
        if showdetailedtime and showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
            print(_output.format(time.asctime(), pos, level, txt))
        elif not showdetailedtime and showinconsole:
            f.write(_output.format(_output.time1(), pos, level, txt))
            print(_output.format(_output.time1(), pos, level, txt))
        elif showdetailedtime and not showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
        else:
            f.write(_output.format(_output.time1(), pos, level, txt))
        f.close()

    def info( txt, pos="main"):
        level = 'INFO'
        f = open(name+".log", "at+")
        if showdetailedtime and showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
            print(_output.format(time.asctime(), pos, level, txt))
        elif not showdetailedtime and showinconsole:
            f.write(_output.format(_output.time1(), pos, level, txt))
            print(_output.format(_output.time1(), pos, level, txt))
        elif showdetailedtime and not showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
        else:
            f.write(_output.format(_output.time1(), pos, level, txt))
        f.close()

    def warn( txt, pos="main"):
        level = 'WARN'
        f = open(name + ".log", "at+")
        if showdetailedtime and showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
            print(_output.format(time.asctime(), pos, level, txt))
        elif not showdetailedtime and showinconsole:
            f.write(_output.format(_output.time1(), pos, level, txt))
            print(_output.format(_output.time1(), pos, level, txt))
        elif showdetailedtime and not showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
        else:
            f.write(_output.format(_output.time1(), pos, level, txt))
        f.close()

    def error( txt, pos="main"):
        level = 'ERROR'
        f = open(name + ".log", "at+")
        if showdetailedtime and showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
            print(_output.format(time.asctime(), pos, level, txt))
        elif not showdetailedtime and showinconsole:
            f.write(_output.format(_output.time1(), pos, level, txt))
            print(_output.format(_output.time1(), pos, level, txt))
        elif showdetailedtime and not showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
        else:
            f.write(_output.format(_output.time1(), pos, level, txt))
        f.close()

    def fatal( txt, pos="main"):
        level = 'FATAL'
        f = open(name + ".log", "at+")
        if showdetailedtime and showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
            print(_output.format(time.asctime(), pos, level, txt))
        elif not showdetailedtime and showinconsole:
            f.write(_output.format(_output.time1(), pos, level, txt))
            print(_output.format(_output.time1(), pos, level, txt))
        elif showdetailedtime and not showinconsole:
            f.write(_output.format(time.asctime(), pos, level, txt))
        else:
            f.write(_output.format(_output.time1(), pos, level, txt))
        f.close()

    def config( name="log", showdetailedtime=False, showinconsole=False):
        name = name
        f = open(name + ".log", "w")
        f.close()
        if not showdetailedtime or showdetailedtime:
            showdetailedtime = showdetailedtime
        else:
            print("wrong detailed time config\nthis config is set to normal")
            showdetailedtime = False
        if not showinconsole or showinconsole:
            showinconsole = showinconsole
        else:
            print("wrong detailed time config\nthis config is set to normal")
            showinconsole = False

    # noinspection PyMethodParameters
    class _output:
        def format(time1, place, level, txt):
            return "[%s] [%s/%s]: %s\n" % (time1, place, level, txt)

        def time1():
            return str(time.localtime().tm_hour).rjust(2, "0")+":" +\
                str(time.localtime().tm_min).rjust(2, "0")+":"+str(time.localtime().tm_sec).rjust(2, "0")
"""

"""
def __init__():
    name = "log"
    f = open(name + ".log", "w")
    f.close()
    showdetailedtime = False
    showinconsole = True
    global name,showdetailedtime,showinconsole
"""
name = "log"
f = open(name + ".log", "w")
f.close()
showdetailedtime = False
showinconsole = True

def debug(txt, pos="main"):
    level = 'debug'
    f = open(name + ".log", "at+")
    if showdetailedtime and showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
        print(_output.format(time.asctime(), pos, level, txt))
    elif not showdetailedtime and showinconsole:
        f.write(_output.format(_output.time1(), pos, level, txt))
        print(_output.format(_output.time1(), pos, level, txt))
    elif showdetailedtime and not showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
    else:
        f.write(_output.format(_output.time1(), pos, level, txt))
    f.close()


def info( txt, pos="main"):
    level = 'INFO'
    f = open(name + ".log", "at+")
    if showdetailedtime and showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
        print(_output.format(time.asctime(), pos, level, txt))
    elif not showdetailedtime and showinconsole:
        f.write(_output.format(_output.time1(), pos, level, txt))
        print(_output.format(_output.time1(), pos, level, txt))
    elif showdetailedtime and not showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
    else:
        f.write(_output.format(_output.time1(), pos, level, txt))
    f.close()


def warn( txt, pos="main"):
    level = 'WARN'
    f = open(name + ".log", "at+")
    if showdetailedtime and showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
        print(_output.format(time.asctime(), pos, level, txt))
    elif not showdetailedtime and showinconsole:
        f.write(_output.format(_output.time1(), pos, level, txt))
        print(_output.format(_output.time1(), pos, level, txt))
    elif showdetailedtime and not showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
    else:
        f.write(_output.format(_output.time1(), pos, level, txt))
    f.close()


def error( txt, pos="main"):
    level = 'ERROR'
    f = open(name + ".log", "at+")
    if showdetailedtime and showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
        print(_output.format(time.asctime(), pos, level, txt))
    elif not showdetailedtime and showinconsole:
        f.write(_output.format(_output.time1(), pos, level, txt))
        print(_output.format(_output.time1(), pos, level, txt))
    elif showdetailedtime and not showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
    else:
        f.write(_output.format(_output.time1(), pos, level, txt))
    f.close()


def fatal( txt, pos="main"):
    level = 'FATAL'
    f = open(name + ".log", "at+")
    if showdetailedtime and showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
        print(_output.format(time.asctime(), pos, level, txt))
    elif not showdetailedtime and showinconsole:
        f.write(_output.format(_output.time1(), pos, level, txt))
        print(_output.format(_output.time1(), pos, level, txt))
    elif showdetailedtime and not showinconsole:
        f.write(_output.format(time.asctime(), pos, level, txt))
    else:
        f.write(_output.format(_output.time1(), pos, level, txt))
    f.close()


def config( name="log", showdetailedtime=False, showinconsole=False):
    name = name
    f = open(name + ".log", "w")
    f.close()
    if not showdetailedtime or showdetailedtime:
        showdetailedtime = showdetailedtime
    else:
        print("wrong detailed time config\nthis config is set to normal")
        showdetailedtime = False
    if not showinconsole or showinconsole:
        showinconsole = showinconsole
    else:
        print("wrong detailed time config\nthis config is set to normal")
        showinconsole = False


# noinspection PyMethodParameters
class _output:
    def format(time1, place, level, txt):
        return "[%s] [%s/%s]: %s\n" % (time1, place, level, txt)

    def time1():
        return str(time.localtime().tm_hour).rjust(2, "0") + ":" + \
            str(time.localtime().tm_min).rjust(2, "0") + ":" + str(time.localtime().tm_sec).rjust(2, "0")
