# -*- coding: utf-8
import os
import click
from tools import load_cfg, save_cfg, daemonize
from colorama import Fore, Back, Style
from ctpips import main as ctpips
import logging
logging.basicConfig(level="INFO")

@click.group()
def cli():
    """vienomics bioinfo standard analysis/operate pipeline
    """
    pass


@cli.command("status")
@click.option("--output", "-o", prompt="output result directory", default="./")
def show_env(output):
    """show status of job running in current path
    """
    import json
    # 检查默认配置
    # print json.dumps(load_cfg(), indent=2)
    config = load_cfg(path=output)
    
    # status = config.get("status", {})
    # print json.dumps(config, indent=2)

    raw_fqs = config.get("raw_fqs", [])
    if not raw_fqs:
        print "no jobs"
        return 
    
    print "%20s\t%20s\n" % ("action", config.get("action"))
    import time
    fmt = "%20s\t%20s\t%20s\t%20s\t%10s"
    print fmt % ("sample_name", "step", "start_at", "end_at", "durations(s)")
    raw_fqs = config.get("raw_fqs", [])
    for sample in raw_fqs:
        config = load_cfg(path=output, cfgfile=sample+".yml")

        status_for_sample = config.get("status", {})
        print json.dumps(config, indent=2)

        steps = status_for_sample.keys()
        steps.sort(lambda a,b : cmp(int(a[0:2]), int(b[0:2])))
        for s in steps:
            start_at, end_at, durations = status_for_sample[s]
            if end_at == 'null' or not end_at:
                end_at = ''
            else:
                end_at = time.strftime("%Y%m%d-%H:%M:%S", time.localtime(float(end_at)))
                durations = int(durations)

            print fmt % (
                sample,
                s,
                time.strftime("%Y%m%d-%H:%M:%S", time.localtime(float(start_at))),
                end_at, durations
            )
            sample = ''

@cli.command("run", short_help="run the default pipeline")
@click.option("--input", "-i", prompt="Directory or fq1", help="process a single[fq1] or batch[Dir] sample")
@click.option("--config", "-c", prompt="Json file", help="config file, only json is supported")
@click.option("--threads", "-t", help="max thread number for every sample", default=8)
@click.option("--output", "-o", help="output result directory", default="./")
@click.option("--fusion", "-f", help="support fusion or not", default=False)
def main(**kw):
    """run the default pipeline
    perl SOP_common.pl -i dir -o dir -t max_thread [--bed 609.bed] --sop conf_XXX.json
    """
    # 检查fq1
    fq1_or_input = kw['input']
    if not os.path.exists(fq1_or_input):
        click.echo(Fore.RED + "%s not exists" % fq1_or_input + Fore.RESET)
        return 

    # 保存配置信息到yml
    kw['update'] = False
    kw['action'] = "run"
    save_cfg(**kw)

    logging.warning(str(kw))
    daemonize(ctpips, cfgpath=kw['output'])


@cli.command("continue")
@click.option("--output", "-o", prompt="output result directory", default="./")
# @click.option("--reason", prompt="why?", default="continue")
def continue_job(output):
    """continue a job 
    """
    config = load_cfg(path=output)
    if not config:
        click.echo(Fore.RED + "cann't find config data!! please run it directly")
        return
    action = config.get("action", "stop")
    if action not in ["pause", "end", "stop"]:
        click.echo(Fore.RED + "operate deny!!!not a paused job!!! action is [%s]" % action + Fore.RESET)
        return

    save_cfg(action="continue", path=output)
    daemonize(ctpips, cfgpath=output)


@cli.command("pause", short_help="pause a running job")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="pause")
def pause_job(**kw):
    """pause a running job
    """
    save_cfg(action="pause", path=kw['output'])


@cli.command("stop", short_help="stop a running job")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="stop")
def stop_job(**kw):
    """stop a running job
    """
    config = load_cfg(path=kw['output'])
    pid = config.get("pid", None)
    if not pid:
        click.echo(Fore.RED + "no running job in path [%s]" % kw.get(output, './'))
        return

    save_cfg(action="stop", path=kw['output'])

    # 根据pid获取pgid
    pgid = os.getpgid(pid)

    # kill -
    os.system("pkill -g %d" % pgid)
    click.echo(Fore.YELLOW + "kill running job [pid:%d][pgid:%d]" % (pid, pgid))
    return


@cli.command("rerun")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="rerun")
def rerun(**kw):
    """rerun a job, if it's running, stop it first!
    """
    config = load_cfg(path=kw['output'])
    # 检查是否存在已有的配置
    if not config:
        click.echo(Fore.RED + "cann't find config data!! please run it directly")
        return
    
    # 检查是否存在正在运行的任务
    action = config.get("action", "run")
    if action in ["run", "continue", "rerun"]:
        click.echo(Fore.RED + "operate deny!!!you should stop the running job first!!!" + Fore.RESET)
        return

    save_cfg(action="rerun", path=kw['output'])
    daemonize(ctpips, cfgpath=kw['output'])

if __name__ == "__main__":
    cli()