# coding=utf8
import os
import yaml
import sys
import atexit
import time

def load_cfg(cfgfile="sop.yml", **kw):
    """load arguments defined by previous calling
    """
    indict = {}
    path = os.path.join(kw.get("path", "./"), '.sop')
    if not os.path.isdir(path):
        return {}

    cfgfile = os.path.join(path, cfgfile)
    if os.path.exists(cfgfile):
        indict = yaml.load(open(cfgfile, 'r'))
    
    # print "load %s from %s" % (str(indict), cfgfile)
    return indict

def save_cfg(**kw):
    """save parameters into a .sop/sop.yml"""
    cfgfile=kw.get("cfgfile", "sop.yml")

    indict = {}
    path = os.path.join(kw.get("path", "./"), '.sop')
    if not os.path.isdir(path):
        os.makedirs(path)

    cfgfile = os.path.join(path, cfgfile)
    if kw.get('update', True):
        if os.path.exists(cfgfile):
            indict = yaml.load(open(cfgfile, 'r'))
        indict.update(kw)
    else:
        indict = kw

    if 'update' in indict:
        del indict['update']

    with open(cfgfile, 'w') as w:
        yaml.dump(indict, w)


def run_cmd(cmd, print_only=True):

    pass

def onexit():
    time.sleep(1)
    print "exit..."

def daemonize(cb=None, pid_file=".pid"):
    """
    创建守护进程
    :param pid_file: 保存进程id的文件
    :return:
    """
    print "in daemonize..."
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
        # os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

    # 写入pid文件
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
            print "pid", os.getpid()    

    if cb:
        print "calling ", cb.__name__
        cb()

        print "calling %s end" % cb.__name__

    # 注册退出函数，进程异常退出时移除pid文件
    atexit.register(onexit)
    sys.exit(0)

if __name__ == "__main__":
    print load_cfg()
    daemonize(load_cfg)
