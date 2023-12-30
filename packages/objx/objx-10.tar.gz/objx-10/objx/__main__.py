#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,E0102,W0611,W0718,W0125


"runtime"


import getpass
import os
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from obj import Default, Object
from prg import Client, Error, Event, Storage
from prg import cmnd, debug, forever, parse_command, scan, spl


from objx import mods as modules


Cfg         = Default()
Cfg.mod     = "cmd,err,mod,mre,pwd,thr"
Cfg.name    = "objx"
Cfg.version = "10"
Cfg.wd      = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")
Cfg.user    = getpass.getuser()


Storage.wd   = Cfg.wd


class Console(Client):

    def announce(self, txt):
        if "v" in Cfg.opts:
            self.say("", txt)

    def poll(self) -> Event:
        evt = Event()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        print(txt)


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


def main():
    Storage.skel()
    parse_command(Cfg, " ".join(sys.argv[1:]))
    if "a" in Cfg.opts:
        Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} started {Cfg.opts.upper()} started {dte}")
    if "d" in Cfg.opts:
        daemon(Cfg.pidfile)
        moddir = os.path.join(Storage.wd, "mods")
        if os.path.exists(moddir) and "m" in Cfg.opts:
            sys.path.insert(0, os.path.dirname(moddir))
            import mods
            if "a" in Cfg.opts:
                Cfg.mod += "," +  ",".join(mods.__dir__())
            scan(mods, Cfg.mod, True)
        privileges(Cfg.user)
        scan(modules, Cfg.mod, True)
        forever()
        return
    if os.path.exists("mods") and "m" in Cfg.opts:
        import mods
        if "a" in Cfg.opts:
            Cfg.mod += "," +  ",".join(mods.__dir__())
        scan(mods, Cfg.mod)
    csl = Console()
    if "c" in Cfg.opts:
        scan(modules, Cfg.mod, True, True)
        csl.start()
        forever()
    if Cfg.otxt:
        scan(modules, Cfg.mod)
        return cmnd(Cfg.otxt)


def wrap(func) -> None:
    old2 = None
    try:
        old2 = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    finally:
        if old2:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old2)


if __name__ == "__main__":
    wrap(main)
    Error.show()
