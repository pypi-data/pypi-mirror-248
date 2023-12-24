# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,W0611,E0102


"main"


import getpass
import inspect
import os
import pwd
import readline
import sys
import termios
import time


sys.path.insert(0, os.getcwd())


from objx import Commands, Default, Errors, Event, Group, Handler, Object, Storage
from objx import cdir, debug, forever, launch, parse_command, spl
from objx import mods as modules


Cfg = Default()
Cfg.mod  = "cmd,dbg,err,fnd,log,mod,mre,pwd,tdo,thr,ver"
Cfg.name = "objx"
Cfg.version = "4"
Cfg.wd = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wd, f"{Cfg.name}.pid")
Cfg.user    = getpass.getuser()


Errors.output = print
Storage.wd = Cfg.wd


class Console(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", Commands.handle)
        Group.add(self)

    def announce(self, txt):
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


def cmnd(txt):
    evn = Event()
    evn.txt = txt
    Commands.handle(evn)
    evn.wait()
    return evn


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


def scan(pkg, modstr, initer=False) -> []:
    mods = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
        mods.append(module)
    return mods


def wrap(func) -> None:
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        sys.stdout.write("\n")
        sys.stdout.flush()
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    Storage.skel()
    parse_command(Cfg, " ".join(sys.argv[1:]))
    if "a" in Cfg.opts:
        Cfg.mods = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        Errors.output = print
    if "d" in Cfg.opts:
        daemon(Cfg.pidfile)
        privileges(Cfg.user)
        scan(modules, Cfg.mod, True)
        forever()
        return
    if "v" in Cfg.opts:
        dte = time.ctime(time.time()).replace("  ", " ")
        debug(f"{Cfg.name.upper()} started {Cfg.opts.upper()} started {dte}")
    csl = Console()
    if "c" in Cfg.opts:
        mods = scan(modules, Cfg.mod, Cfg.hasmods)
        if "w" in Cfg.opts:
            for mod in mods:
                if "_thr" in dir(mod):
                    mod._thr.join()
        if "t" in Cfg.opts:
            csl.threaded = True
        csl.start()
        forever()
        return
    scan(modules, Cfg.mod)
    cmnd(Cfg.otxt)


def wrapped():
    wrap(main)
    Errors.show()

if __name__ == "__main__":
    wrapped()
