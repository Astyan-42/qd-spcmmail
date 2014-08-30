#!/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

import config
from classes.mysqlpostfix import mysqlpostfix
from classes.filepostfix import filepostfix
from classes.security import security
from classes.courier import courier
from classes.useranddomain import useranddomain

class manage:
    
    def __init__(self):
        self.mpostfix = mysqlpostfix()
        self.fpostfix = filepostfix()
        self.security = security()
        self.courier = courier()
        
    def restart(self):
        subprocess.call("/etc/init.d/courier-authdaemon restart", shell = True)
        subprocess.call("/etc/init.d/courier-imap restart", shell = True)
        subprocess.call("/etc/init.d/courier-imap-ssl restart", shell = True)
        subprocess.call("/etc/init.d/courier-pop restart", shell = True)
        subprocess.call("/etc/init.d/courier-pop-ssl restart", shell = True)
        subprocess.call("/etc/init.d/saslauthd restart", shell = True)
        subprocess.call("service postfix restart", shell = True)
        
    def startrow(self):
        self.uandd = useranddomain()
        for domain in config.domainstart:
            try:
                self.uandd.addDomain(domain)
            except:
                pass
        for (address, passwd) in config.usersstart:
            try:
                self.uandd.addUser(address, passwd)
            except:
                pass
                

    def makeInstall(self):
        self.mpostfix.createAll()
        self.fpostfix.createAll()
        self.security.createAll()
        self.courier.replaceAuthmysqlrcConf()
        self.courier.replaceAuthdaemonrcConf()
        self.startrow()
        self.restart()
    
    def makeUninstall(self):
        self.mpostfix.deleteAll()
        self.fpostfix.deleteAll()
        self.security.deleteAll()
    
    def choose(self):
        if len(sys.argv) == 1:
            return
        else:
            if sys.argv[1] == "install":
                self.makeInstall()
            elif sys.argv[1] == "uninstall":
                self.makeUninstall()
            elif sys.argv[1] == "adddomain":
                self.uandd = useranddomain()
                if len(sys.argv) == 3:
                    self.uandd.addDomain(sys.argv[2])
            elif sys.argv[1] == "addalias":
                self.uandd = useranddomain()
                if len(sys.argv) == 4:
                    self.uandd.addAlias(sys.argv[2],sys.argv[3])
            elif sys.argv[1] == "adduser":
                self.uandd = useranddomain()
                if len(sys.argv) == 4:
                    self.uandd.addUser(sys.argv[2],sys.argv[3])
                
if __name__ == '__main__':
    t = manage()
    t.choose()
            
    
    
