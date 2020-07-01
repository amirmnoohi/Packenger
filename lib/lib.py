import os
import sys
import time
from multiprocessing import Process


def change_sudo():
    if os.geteuid() != 0:
        print(bcolors.FAIL + "[-] Script is not started as root." +
              bcolors.ENDC)
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def wait(length=0.1104):
    try:
        time.sleep(length)
    except KeyboardInterrupt:
        pass


def loading(text, speed):
    try:
        while True:
            print (bcolors.OKBLUE + "\r" + "[-] " + text + bcolors.ENDC)
            sys.stdout.write("\033[F")
            wait(speed)
            print(bcolors.OKBLUE + "\r" + "[\\] " + text + bcolors.ENDC)
            sys.stdout.write("\033[F")
            wait(speed)
            print(bcolors.OKBLUE + "\r" + "[|] " + text + bcolors.ENDC)
            sys.stdout.write("\033[F")
            wait(speed)
            print(bcolors.OKBLUE + "\r" + "[/] " + text + bcolors.ENDC)
            sys.stdout.write("\033[F")
            wait(speed)

    except KeyboardInterrupt:
        exit(0)


def pstart(text, speed):
    p = Process(target=loading, args=(text, speed,))
    p.start()
    return p


def pstop(p, timeout=3):
    wait(timeout)
    sys.stdout.write("\r")
    p.terminate()


def clean():
    sys.stdout.write("\033[F")


space = "
