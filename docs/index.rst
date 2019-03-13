============
sop
============


Introduction
============

sop is used to ....


Authors
=======

.. _authors:
    
    KongDeju <kongdeju@gene.ac>



Status
======

.. note::

    **not reviewed yet.**



Installation
============

use git to clone code::

    git clone git@123.57.226.13:/expan/DevRepos/sop.git


..  attention::

    if you want to run ``sop`` on local server without docker , try to add ``config.py``.


Usage
=====

    
just type command::

    /path/to/sop.py -h


developments followed by ``Dcer`` rules, script will need a yaml file,which shoud contain following key and values

must_args
---------

- args1
    desc of args2

- args2
    desc of args2
 
optinal args
------------

- args3
    desc of args3


here is a sample yaml file::

    args1: value of args1
    args2: value of args2


RUN
===

cli way
-------

copy and paste to your input yaml file and call script::

    /path/of/sop.py -c your.yml


serer way
---------

send request to jbios with ``/start/sop/``::

    req = requests.get("http://<server>:port/sop/",data=json.dumps(indict))

for jbios detail information check api documentation `here <http://jbio.cc:6636/dev-docs/jbios/>`_


Tests
=====

check test report `here <http://jbio.cc:6636/dev-tests/sop/>`_

download testdata `here <http://jbio.cc:6636/dev-tests/sop/testData.tgz>`_

Report
======

check sample report `here <http://jbio.cc:6636/dev-report/sop/html/>`_


Code
====

.. toctree::
   :maxdepth: 1

    Guide <index>
    Code Docs <api/modules>
