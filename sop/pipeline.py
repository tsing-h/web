import os
import threading
import re
class pipeline(object):

    def __init__(self, config=None):
        self.config = dict(config)
        self._pipe = []
        return self

    def config(self, config=None):
        self.config = dict(config)
        
        return self

    def pipeline(callback):
        self._pipe.append(list(callback))
        return self

    def run(self):
        while self._pipe:
            cbs = self._pipe.pop(0)
            for cb in cbs:
                # 创建子进程，执行命令，等待返回
                cb(self.config)
        
        

class ctpip(threading.Event):

    def __init__(self, fq1, path2cmd):
        """init a ctpip pipeline
        Arguments:
            fq1: the R1 fastq
            path2cmd: the path for the external scripts, eg: 
        """
        self.fq1 = fq1
        self.prefix = re.split(r'_R1', os.path.basename(f))[0]


if __name__ == "__main__":
    pass