# -*- coding: utf-8
import os
from tools import load_cfg, save_cfg
# from pipeline import pipeline
import time
import json
import re
from colorama import Fore, Back, Style
from glob import glob
from multiprocessing import Process, Lock
import logging
from collections import defaultdict
import subprocess as sp

# from ctpips.dedup import dedup_sop as dedup
# from ctpips.merge import merge
# from ctpips.calling import varscan_call as call_variations

# path2script = "/4_disk/software/softs/private/sop"
path2script = "/home/sop/609"
script_fusion = "/home/YHbioinfo/pipeline_version_2/fusion/run_fusion_with_bam.py"
sleep_time = 10 

def run_cmd(cmd, print_only=False):
    """在当前进程执行命令，等待命令结果，收集命令输出信息
    """
    logging.info("[cmd] " + cmd)
    print Fore.YELLOW+cmd+Fore.RESET
    if print_only:
        return cmd
    # ret = sp.check_output(cmd, shell=True, stderr=sp.STDOUT)
    ret = sp.check_output(cmd, shell=True)
    return ret


def preprocess(ymlfile, cfgpath="./"):
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    fq1, output, thread = config['fq1'], config['output'], config['threads']
    sample_prefix = config.get("sample_prefix", fq1)

    merge, sample_type = "--nomerge", ""
    if re.search(r'cf', sample_prefix.lower()):
        merge = '--merge'
        sample_type = "cf"
        
    fusion = "--nofusion" if not config.get('fusion', False) else '--fusion' 

    # # perl /home/sop/609/clean_merge_common.pl -fq1 {fq1} -o {path} -t {thread} {merge} {fusion}
    cmd = "perl %s/clean_merge_common.pl -fq1 %s -o %s -t %d %s %s" % (path2script, fq1, output, thread, merge, fusion)
    ret = run_cmd(cmd)

    # 产生了哪些文件?
    formatted_fastqs = {
        "merged": os.path.join(output, sample_prefix+"_merge_R1.fastq"),
        "logs": ret
    }
    clean_fq = os.path.join(output, 'fusion', sample_prefix+"_barcode_R1.fastq")
    if os.path.exists(clean_fq):
        formatted_fastqs["clean"] = clean_fq
    
    t80bp_fq = os.path.join(output, 'fusion', sample_prefix+"_80bp_R1.fastq")
    if os.path.exists(t80bp_fq):
        formatted_fastqs["80bp"] = t80bp_fq

    save_cfg(cfgfile=ymlfile, path=cfgpath, formatted_fastqs=formatted_fastqs, sample_type=sample_type)
    return ret

def bwa_map(fq1,  fq2='', threads=8, ref='', sam='', bam=''):
    if not fq2:
        fq2 = "%s_R2%s" % tuple(re.split(r'_R1', fq1))
    
    cmd = ''
    if sam:
        cmd = "bwa mem -t {0} -M {1} {2} {3} > {4}".format(threads, ref, fq1, fq2, sam)
    else:
        cmd = "bwa mem -t {0} -YM {1} {2} {3} | samtools view -Su -@ {0}|samtools sort -@ {0} -o {4}".format(threads, ref, fq1, fq2, bam)
    rst = run_cmd(cmd)
    if bam:
        cmd = "samtools index %s" % bam
        run_cmd(cmd)

    return rst

def mapping(ymlfile, cfgpath="./"):
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    fq1, output, thread, ref = config['fq1'], config['output'], config['threads'], config['ref']
    sample_prefix = config.get("sample_prefix", fq1)

    formatted_fastqs = config["formatted_fastqs"]

    logs = ""
    first_maped = {}
    # 处理fusion
    if formatted_fastqs.get("80bp", ''):
        fq_80bp = formatted_fastqs['80bp']
        first_maped["80bp"] = os.path.join(output, 'fusion', sample_prefix+"_80bp_sort.bam")
        rst = bwa_map(fq_80bp, threads=config['threads'], ref=config['ref'], bam=first_maped["80bp"])
        # logs += str(rst)+"\n"

    # 为减少磁盘占用，无dup时，clean_merge不会生成额外的clean_fastq
    if formatted_fastqs.get("clean", ''):
        fq_clean= formatted_fastqs['clean']
        first_maped["clean"] = os.path.join(output, 'fusion', sample_prefix+"_clean_sort.bam")
        rst = bwa_map(fq_clean, threads=config['threads'], ref=config['ref'], bam=first_maped["clean"])
        # logs += str(rst)+"\n"

    # 处理去冗余cf样本
    sample_type = config.get("sample_type", None)
    dup = config.get("dup", 0)
    fq_merged= formatted_fastqs['merged']
    if dup and sample_type == "cf":
        # 生成sam文件
        first_maped["merged"] = os.path.join(output, sample_prefix+".sam")
        rst = bwa_map(fq_merged, threads=config['threads'], ref=config['ref'], sam=first_maped["merged"])
        # logs += str(rst)+"\n"
        # 存在80bp但不存在clean时，需要将sam转为bam
        if formatted_fastqs.get("80bp", '') and not formatted_fastqs.get("clean", ''):
            # samtools view -Su -@ $cur_bwa_threads $file_merge_sam |$samtools sort -@ $cur_bwa_threads -o $file_merge_bam
            first_maped["clean"] = os.path.join(output, 'fusion', sample_prefix+"_clean_sort.bam")
            cmd = "samtools view -Su -@ {0} {1}|samtools sort -@ {0} -o {2}".format(config['threads'], first_maped["merged"], first_maped["clean"])
            rst = run_cmd(cmd)
            # logs += str(rst)+"\n"
    else:
        first_maped["merged"] = os.path.join(output, sample_prefix+".bam")
        rst = bwa_map(fq_merged, threads=config['threads'], ref=config['ref'], bam=first_maped["merged"])
        # logs += str(rst)+"\n"
    
    first_maped['logs'] = logs
    save_cfg(cfgfile=ymlfile, path=cfgpath, first_maped=first_maped)
    return logs

def dedup(ymlfile, cfgpath="./"):
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    dup, sample_type = config.get('dup', 0), config['sample_type']
    first_maped = config['first_maped']

    file_merged, deduped = first_maped['merged'], {}
    bed = config.get("bed", config.get("panel", ''))
    if not bed:
        raise Exception("no bed/panel")

    if not (dup and sample_type=="cf"):
        # 不需要dup， perl ontarget.pl {bed} {file_bam}
        logging.info("sample [%s] don't need dedup" % config['sample_prefix'])
        cmd = "perl {0}/ontarget.pl {1} {2}".format(path2script, bed, file_merged)
        deduped['logs'] = run_cmd(cmd)
        save_cfg(cfgfile=ymlfile, path=cfgpath, deduped=deduped)
        return deduped['logs']
    
    # 执行dup
    logs = ""
    output, sample_prefix = config['output'], config["sample_prefix"]
    # sam -> fastq perl sam_barcode_duplicate_2.0.pl {file_merge_sam} {bed}
    cmd = "perl {0}/sam_barcode_duplicate_2.0.pl {1} {2}".format(path2script, file_merged, bed)
    deduped['dup_fq'] = os.path.join(output, sample_prefix+"_3rongyu_R1.fastq")
    rst = run_cmd(cmd)
    logs += str(rst)

    # dup_fastq -> bam
    deduped['dup_bam'] = os.path.join(output, sample_prefix+".bam")
    rst = bwa_map(deduped['dup_fq'], threads=config['threads'], ref=config['ref'], bam=deduped['dup_bam'])
    logs += str(rst)
    deduped['logs'] = run_cmd(cmd)
    save_cfg(cfgfile=ymlfile, path=cfgpath, deduped=deduped)

    # 删除fastq文件
    cmd = "echo rm -f %s" % os.path.join(output, sample_prefix+"_3rongyu_R*.fastq")
    run_cmd(cmd)

    # TODO 转换sam到bam， 删除sam文件

    return logs


def fusion(ymlfile, cfgpath="./"):
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    # dup, sample_type = config.get('dup', 0), config['sample_type']
    
    fusion = config.get("fusion", 0)
    if not fusion:
        logging.info("sample [%s] don't need dedup" % config['sample_prefix'])
        return
    
    first_maped = config['first_maped']
    # 确认bam文件 80bp,clean
    bam_80bp  = first_maped.get("80bp", None)
    bam_clean = first_maped.get("clean", None)
    if bam_80bp and not bam_clean:
        bam_clean = first_maped.get("merged", None)
    cmd = "python {0} -b {1} -C {2} -o {3} -p {4}" % (script_fusion, bam_clean, bam_80bp, os.path.join(config['output'], "fusion"), config['sample_prefix'])
    run_cmd(cmd)

    # 清理中间文件
    cmd = "echo rm -f %s" % (os.path.join(config['output'], 'fusion', "*bam"))
    run_cmd(cmd)
    return


def call_mutations(ymlfile, cfgpath="./"):
    """call variation by samtools
    """
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    deduped, first_maped = config['deduped'], config['first_maped']
    bam = deduped.get("dup_bam", None)
    if not bam:
        bam = first_maped['merged']

    output, sample_prefix = config['output'], config['sample_prefix']
    mpileuped = {
        "mpileup": os.path.join(output, sample_prefix+".mpileup")
    }
    cmd = "samtools mpileup -BQ 10 -d 500000 -f {0} {1} > {2}".format(
        config['ref'], bam, mpileuped['mpileup']
    )
    run_cmd(cmd)

    # mpielup -> txt
    bed = config.get("bed", config.get("panel", ''))
    database = config.get("database")
    adjust = "--noadjust"
    if not config.get("dup", 0) and config.get("sample_type", "") == "cf":
        adjust = "--adjust"
    # perl mpileup_analysis_609.pl {mpileup} --output {output/out/} -u --bed {bed} --database {db} {adjust}
    cmd = "perl {0}/mpileup_analysis_609.pl {1} --output {2} -u --bed {3} --database {4} {5}".format(
        path2script, mpileuped['mpileup'], os.path.join(output, 'out'), bed, database, adjust
    )
    mpileuped['mutation'] = os.path.join(output, 'out', sample_prefix+".mpout_v2.1.txt")
    mpileuped['stat'] = os.path.join(output, 'out', sample_prefix+"_stat.txt")
    rst = run_cmd(cmd)
    mpileuped['logs'] = rst
    save_cfg(cfgfile=ymlfile, path=cfgpath, mpileuped=mpileuped)
    return rst


def postprocess(ymlfile, cfgpath="./"):
    """生成统计信息
    """
    config = load_cfg(cfgfile=ymlfile, path=cfgpath)
    mpileuped = config['mpileuped']

    # Rscript statistics_mpileup_depth.R {stat.txt}
    cmd = "Rscript {0}/statistics_mpileup_depth.R {1}".format(
        path2script, mpileuped['stat']
    )
    rst = run_cmd(cmd)
    statistics = {
        "logs": rst 
    }
    save_cfg(cfgfile=ymlfile, path=cfgpath, statistics=statistics)


def ctpip(sample_prefix, cfgpath="./", filelock=None):
    """处理单个样本

    按预设流程处理单个样本
    从默认配置文件中读取控制信息，决定是继续还是停止
    从指定配置文件中读取当前样本已处理的进度
    """
    # stage and process
    state_transitions = [preprocess, mapping, dedup, fusion, call_mutations, postprocess]

    cfgfile = sample_prefix+".yml"
    config = load_cfg(cfgfile=cfgfile, path=cfgpath)
    for stage, process in enumerate(state_transitions):
        str_stage = "%02d-%s" % (stage, process.__name__)
        # 处理全局指令
        global_config = load_cfg(path=cfgpath)
        if not global_config:
            try_times= 0
            # 指数等待，3次后不再尝试
            while not global_config and try_times < 5:
                logging.debug("try fetch global config in 2^%d s" % try_times)
                time.sleep(pow(2, try_times))
                try_times += 1
                global_config = load_cfg(path=cfgpath)

        if not global_config:
            raise Exception("load_cfg: can not load data")

        # 运行中的子任务，只需处理pause
        if global_config['action'] == "pause":
            logging.info("pausing...")
            return

        # 检查当前模块是否已处理过
        status = config.get("status", defaultdict(list))

        # logging.info("check current stage" + str(status))
        if str_stage in status and status[str_stage][1] != None:
            logging.info("skip current stage" + str_stage)
            logging.info("status: " + str(status[str_stage]))
            continue
        
        # logging.info("rerun step" + str_stage)
        # return 

        # 执行当前模块
        begin_at = time.time()
        current = {
            "stage": str_stage,
            "start_at": begin_at
        }
        status[str_stage] = [begin_at, None, "running"]
        save_cfg(cfgfile=cfgfile, current=current, status=status, path=cfgpath)
        
        # rst = process(cfgfile, cfgpath=cfgpath)
        try:
            rst = process(cfgfile, cfgpath=cfgpath)
        except Exception as e:
            logging.critical("Error occured in %s %s" % (str_stage, str(e)))
            status[str_stage] = [begin_at, None, str(e)]
            save_cfg(cfgfile=cfgfile, current=current, status=status, path=cfgpath)
            return 
        
        logging.info("[result for %s] %s" % (str_stage, str(rst)))

        # 设置状态: 在prefix.yml中记录详细信息
        end_at = time.time()
        current['end_at'] = end_at
        status[str_stage] = [begin_at, end_at, end_at-begin_at]
        save_cfg(cfgfile=cfgfile, current=current, status=status, path=cfgpath)
        

def main(cfgpath="./"):
    lock = Lock()
    # 获取待处理样本或目录
    config = load_cfg(path=cfgpath)
        
    fq1_or_input = config.get("input")
    fs, raw_fqs = [], {}
    if os.path.isdir(fq1_or_input):
        fs = glob(os.path.join(fq1_or_input, "*R1*f*q*"))
    else:
        fs = [fq1_or_input]
    # print "fs:", fs
    json_file, json_config = config['config'], {}
    if json_file:
        json_config = json.load(open(json_file))[0]
        # print json.dumps(json_config, indent=2)

    # run, continue, rerun三种状态
    action = config.get("action", "run")
    # run: 从新生成子配置文件, 开始运行
    tasks = []
    for f in fs:
        if not f.endswith(("fastq", "fastq.gz", "fq", "fq.gz")):
            continue
        prefix = re.split(r'_R1', os.path.basename(f))[0]
        # sample_type = "cf"
        raw_fqs[prefix] = f

        if action in ["run", "rerun"]:
            # 创新新的子配置文件, 覆盖原有的配置文件
            sample_cfg = { 
                "status": {}, 
                "sample_prefix": prefix, 
                "fq1": f,
                # "type": "cf",
                # "json": config['config'],
                "threads": config['threads'],
                "output": config['output']
            }
            sample_cfg.update(json_config)
            # print Fore.RED+"init config file %s/%s" % (cfgpath, prefix) + Fore.RESET
            save_cfg(path=cfgpath, cfgfile=prefix+".yml", update=False, **sample_cfg)
        else:
            logging.debug("continue job")

        # cpu密集型任务优先用多进程， io密集和网络密集型优先用多线程
        logging.debug("start new process for sample:" + prefix)
        p = Process(target=ctpip, args=(prefix, cfgpath, lock))
        p.start()
        tasks.append(p)


    # 记录进程ID到全局配置中
    save_cfg(path=cfgpath, raw_fqs=raw_fqs, action=action, pid=os.getpid(), filelock=lock)

    for t in tasks:
        t.join()

    save_cfg(path=cfgpath, action="end", filelock=lock)
    logging.debug("main pipeline ending...")