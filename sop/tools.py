# coding=utf8
import os
import yaml
import sys
import atexit
import time
import logging
from shutil import move
from colorama import Fore, Back, Style

def load_cfg(cfgfile="sop.yml", **kw):
    """load arguments defined by previous calling
    """
    indict = {}
    debug = kw.get("debug", False)

    path = os.path.join(kw.get("path", kw.get("output", "./")), '.sop')
    if not os.path.isdir(path):
        return {}

    cfgfile = os.path.join(path, cfgfile)
    # print Fore.YELLOW+"load cfg from [ " + cfgfile + " ]" + Fore.RESET

    if os.path.exists(cfgfile):
        with open(cfgfile, 'r') as r:
            indict = yaml.load(r)
        if not indict:
            # print Fore.YELLOW+"sleep for 3" + Fore.RESET
            time.sleep(3)

            with open(cfgfile, 'r') as r:
                indict = yaml.load(r)

    # print cfgfile
    return indict

def save_cfg(**kw):
    """save parameters into a .sop/sop.yml"""
    cfgfile=kw.get("cfgfile", "sop.yml")

    indict = {}
    path = os.path.join(kw.get("path", kw.get("output", "./")), '.sop')
    if not os.path.isdir(path):
        os.makedirs(path)

    cfgfile = os.path.join(path, cfgfile)
    # 使用锁控制多个进程同时写入文件，导致先写的数据被覆盖, 确保读最新数据
    lock = kw.get("filelock", None)
    if lock:
        del kw['filelock']
        lock.acquire()

    if kw.get('update', True):
        if os.path.exists(cfgfile):
            with open(cfgfile, 'r') as r:
                indict = yaml.load(r)
        indict.update(kw)
    else:
        indict = kw

    if 'update' in indict:
        del indict['update']

    # 写入新的文件，用新的文件替换原来的文件。 读文件过程中被覆盖了会怎么样? 
    # cfgfile_bake = cfgfile+"~"
    # with open(cfgfile_bake, 'w') as w:
    #     yaml.dump(indict, w)
    #     w.flush()
    # # os.system("mv %s %s" % (cfgfile_bake, cfgfile))
    # move(cfgfile_bake, cfgfile)

    with open(cfgfile, "w") as w:
        yaml.dump(indict, w)
        w.flush()

    # print Fore.GREEN+"save cfg from [ " + cfgfile_bake + " ] to [ " + cfgfile + " ]" + Fore.RESET
    if lock:
        lock.release()

def run_cmd(cmd, print_only=True):
    pass

def onexit():
    logging.debug("exit...")

def daemonize(cb=None, pid_file=".pid", debug=False, **kw):
    """
    创建守护进程
    :param pid_file: 保存进程id的文件
    :return:
    """
    logging.debug("in daemonize...")
    if not debug:
        pid = os.fork()
        if pid:
            # 结束父进程，将自己交给操作系统的init
            sys.exit(0)

        # 子进程默认继承父进程的工作目录，最好是变更到根目录，否则回影响文件系统的卸载
        # os.chdir('/')
        # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
        # os.umask(0)
        # 让子进程成为新的会话组长和进程组长
        os.setsid()
        # 防止异常, 再次fork下
        _pid = os.fork()
        if _pid:
            sys.exit(0)

        # 此时，进程已经是守护进程了，接下来重定向标准输入、输出、错误的描述符(是重定向而不是关闭, 这样可以避免程序在 print 的时候出错)

        # 刷新缓冲区先，小心使得万年船
        sys.stdout.flush()
        sys.stderr.flush()

        # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
        with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())

    # 写入pid文件
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
            logging.debug("pid %d" % os.getpid())

    if cb:
        logging.debug("calling %s" % cb.__name__)
        cb(**kw)

        logging.debug("calling %s end" % cb.__name__)

    # 注册退出函数，进程异常退出时移除pid文件
    atexit.register(onexit)
    sys.exit(0)

if __name__ == "__main__":
    print load_cfg()
    daemonize(load_cfg)
