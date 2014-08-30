#!/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

sys.path[:0] = ['../']

import config

class courier:
    
    def __init__(self):
        pass
    
    def replaceAuthmysqlrcConf(self):
        conf = open(os.path.join(config.courierdir,"authmysqlrc"),"w")
        conf.writelines(config.authmysqlrc)
    
    def replaceAuthdaemonrcConf(self):
        conf = open(os.path.join(config.courierdir,"authdaemonrc"),"w")
        conf.writelines(config.authdaemonrc)
        
