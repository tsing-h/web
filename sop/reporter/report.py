try:
    from config import render
    from config import md2html
except:
    render = "render.py"
    md2html = "md2html.py"
from jbiot import log
import os
from jbiot import jbiotWorker
from jbiot import get_template
from jbiot import yamladd
import yaml
import json

def report(ymlfile):
    """ sop to markdown file and html file

    """
    # handle input
    indict = yaml.load(open(ymlfile))

    render_yml = "sop_render.yml"
    cmd = "echo '%s' > %s" % (json.dumps(indict),render_yml)
    log.run("get sop args to render",cmd)

    templ = get_template("sop")
    out = "sop.md"
    cmd = "%s -t %s -j %s -o %s -y" % (render,templ,render_yml,out)
    log.run("render sop template",cmd,docker="jbioi/report",singularity="report.img")
    
    cmd = "%s %s" % (md2html,out)
    log.run("md2html sop ",cmd,docker="jbioi/report",singularity="report.img")
    outdict = {}
    outdict["sop"] = out
    yamlout = yamladd(yamlin,outdict)
    yamlout["sop_outdir"] = os.getcwd()
    return ymlfile
