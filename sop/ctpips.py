# -*- coding: utf-8
import os
from tools import load_cfg, save_cfg
# from pipeline import pipeline
import time
import json
import re
from colorama import Fore, Back, Style
from glob import glob
from multiprocessing import Process


path2script = "/4_disk/software/softs/private/sop/"

def run_cmd(cmd, print_only=True):
    print(Fore.YELLOW+cmd)
    if not print_only:
        os.system(cmd)


def preprocess():
    print "in preprocess"
    # config = load_cfg()
    # fq1, output, thread = config['fq1'], config['output'], config['threads']
    # merge = "--merge"
    # if re.search(r'cf', fq1.lower()):
    #     merge = '--nomerge'
    # fusion = "--nofusion" if not config.get('fusion', False) else '--fusion' 

    # # perl /home/sop/609/clean_merge_common.pl -fq1 {fq1} -o {path} -t {thread} {merge} {fusion}
    # cmd = "perl %s/clean_merge_common.pl -fq1 %s -o %s -t %d %s %s" % (fq1, output, thread, merge, fusion)
    # run_cmd(cmd)
    time.sleep(3)

    # 产生了哪些文件?

    pass


def mapping(f):
    print "in mapping"
    time.sleep(3)
    
    pass


def dedup():
    print "in dedup"
    time.sleep(3)
    pass


def fusion():
    print "in fusion"
    time.sleep(3)
    pass


def postprocess():
    print "in postprocess"
    time.sleep(3)
    pass


def ctpip(sample_code):
    """处理单个样本

    按预设流程处理单个样本
    从默认配置文件中读取控制信息，决定是继续还是停止
    从指定配置文件中读取当前样本已处理的进度
    """
    # stage and process
    state_transitions = [preprocess, mapping,  dedup, fusion, postprocess]
    while True:
        # 从默认配置中读取控制信息
        default_config = load_cfg()
        cfgfile = sample_prefix+".yml"
        print "\n========Sample: %s Action: %s==========" % (sample_code, default_config['action'])
        
        # 运行中的子任务，只需处理pause
        if default_config['action'] == "pause":
            print "pause..."
            save_cfg(cfgfile=cfgfile, status="paused")
            return

        config = load_cfg(cfgfile=cfgfile)
        stage =  config.get("stage", 0)
        if stage >= len(state_transitions):
            print "Sample: %s ending...", stage
            save_cfg(cfgfile=cfgfile, stage=0)

            # return
            continue

        process = state_transitions[stage]
        current = {
            "stage" : stage,
            "function": process.__name__,
            "statues": "running"
        }
        print current

        
        begin_at = time.time()
        save_cfg(current=current)
        end_at = time.time()
        # process()

        save_cfg(stage=stage+1)

def ctpips():
    # 获取待处理样本或目录
    config = load_cfg()

    fq1_or_input = config.get("input")
    fs, raw_fqs = [], {}
    if os.path.isdir(fq1_or_input):
        fs = glob(os.path.join(fq1_or_input, "R1*f*q*"))
    else:
        fs = [fq1_or_input]


    # run, continue, rerun三种状态
    action = config.get("action", "run")
    # run: 从新生成子配置文件, 开始运行
    tasks = []
    for f in fs:
        if not f.endswith(("fastq", "fastq.gz", "fq", "fq.gz")):
            continue
        prefix = re.split(r'_R1', os.path.basename(f))[0]

        raw_fqs[prefix] = f
        if action in ["run", "rerun"]:
            # 创新新的子配置文件, 覆盖原有的配置文件
            sample_cfg = { 
                "status": "ready", 
                "stage": 0, 
                "sample_code": prefix, 
                "fq1": f,
                "json": config['config'],
                "threads": config['threads'],
                "output": config['output']
            }
            save_cfg(cfgfile=sample_prefix+".yml", update=False, **sample_cfg)

        # cpu密集型任务优先用多进程， io密集和网络密集型优先用多线程
        print "start new process for sample:", prefix
        p = Process(target=ctpips, args=(prefix,))
        p.start()
        tasks.append(p)

    save_cfg(raw_fqs=raw_fqs, action=action, status="running", pid=os.getpid())

    for t in tasks:
        t.join()

    # 再次检查状态
    config = load_cfg()
    status = ""
    if action in ["run", "rerun", "continue"]:
        status="success ending"
    elif action == "pause":
        status = "paused"
    else:
        status = "stopped"
    save_cfg(status=status)
    print "main pipeline ending..."