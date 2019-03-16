# -*- coding: utf-8
import os
import click
from tools import load_cfg, save_cfg, daemonize
from colorama import Fore, Back, Style
from ctpips import ctpips

@click.group()
def cli():
    """vienomics bioinfo standard analysis/operate pipeline
    """
    pass


@cli.command("status")
def show_env():
    """show status of job running in current path
    """
    import json
    print json.dumps(load_cfg(), indent=2)


@cli.command("run", short_help="run the default pipeline")
@click.option("--input", "-i", prompt="Directory or fq1", help="process a single[fq1] or batch[Dir] sample")
# @click.option("--fq1", "-1", prompt="the R1 fastq, gzip is supported", )
# @click.option("--prefix", "-p", prompt="the prefix", default=None)
@click.option("--config", "-c", prompt="Json file", help="config file, only json is supported")
@click.option("--threads", "-t", help="max thread number for every sample", default=8)
@click.option("--output", "-o", help="output result directory", default="./")
def main(**kw):
    """run the default pipeline
    perl SOP_common.pl -i dir -o dir -t max_thread [--bed 609.bed] --sop conf_XXX.json
    """
    # 检查fq1
    fq1_or_input = kw['input']
    if not os.path.exists(fq1_or_input):
        click.echo(Fore.RED + "%s not exists" % fq1_or_input)
        return 

    # config['raw'] = {
        # "fq1" : fq1
    # }

    # 保存配置信息到yml
    kw['update'] = False
    save_cfg(**kw)
    print str(kw)
    daemonize(ctpips)


@cli.command("continue")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="continue")
def continue_job():
    """continue a job 
    """
    config = load_cfg()
    if not config:
        click.echo(Fore.RED + "cann't find config data!! please run it directly")
        return
    
    if not config.get("pause", False):
        click.echo(Fore.RED + "operate deny!!!")
        return
    config['pause'] = False
    save_cfg(**config)
    daemonize(ctpips)


@cli.command("pause", short_help="pause a running job")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="pause")
def pause_job(**kw):
    """pause a running job
    """
    save_cfg(pause=True, current={"reason":kw['reason'], "state": "pause"})


@cli.command("stop", short_help="stop a running job")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="stop")
def stop_job(**kw):
    """stop a running job
    """
    config = load_cfg()
    pid = config.get("pid", None)
    if not pid:
        click.echo(Fore.RED + "no running job in path [%s]" % kw.get(output, './'))
        return 
    os.system("kill %d" % pid)
    click.echo(Fore.YELLOW + "kill running job [pid = %d]" % pid)
    return


@cli.command("rerun")
@click.option("--output", "-o", prompt="output result directory", default="./")
@click.option("--reason", prompt="why?", default="rerun")
def rerun(**kw):
    """rerun a job, if it's running, stop it first!
    """
    config = load_cfg()
    if not config:
        click.echo(Fore.RED + "cann't find config data!! please run it directly")
        return
    
    if not config.get("pause", False):
        click.echo(Fore.RED + "operate deny!!!")
        return
    config['pause'] = False
    config['stage'] = 0
    save_cfg(**config)
    daemonize(ctpips)

if __name__ == "__main__":
    cli()