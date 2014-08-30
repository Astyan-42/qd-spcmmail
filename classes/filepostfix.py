#!/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import shutil

sys.path[:0] = ['../']

import config

class filepostfix:
    
    def __init__(self):
        pass
    
    def createGroupAndUser(self):
        subprocess.call("groupadd -g "+str(config.vmailid)+" vmail",shell=True)
        subprocess.call("useradd -g vmail -u "+str(config.vmailid)+" vmail -d "+config.vmaildir+" -m",shell=True)
    
    def deleteGroupAndUser(self):
        subprocess.call("userdel vmail",shell=True)
        subprocess.call("groupdel vmail",shell=True)
        try:
            shutil.rmtree(config.vmaildir)
        except:
            pass
    
    def changeMaster(self):
        master = open(os.path.join(config.postfixdir, "master.cf"),"w")
        master.writelines(config.postfixmaster)

    def createPostfixConfigFiles(self):
        for postfixfile in config.postfixconfigfiles:
            f = open(os.path.join(config.postfixdir, postfixfile[0]),"w")
            f.writelines(postfixfile[1])
            os.chmod(os.path.join(config.postfixdir, postfixfile[0]),0640)
            subprocess.call("chgrp postfix "+os.path.join(config.postfixdir, postfixfile[0]),shell=True)
        
    def deletePostfixConfgFiles(self):
        for postfixfile in config.postfixconfigfiles:
            try:
                os.remove(os.path.join(config.postfixdir, postfixfile[0]))
            except:
                pass
    
    def createLinks(self):
        subprocess.call("mkdir -p /var/spool/postfix/var/run/mysqld", shell=True)
        subprocess.call("chown mysql /var/spool/postfix/var/run/mysqld", shell=True)
        subprocess.call("ln -s /var/run/mysqld/mysqld.sock /var/spool/postfix/var/run/mysqld/mysqld.sock", shell=True)
        #~ subprocess.call("ln -s /usr/lib/postfix/proxymap /var/spool/postfix/private/proxymap", shell=True)
        
        subprocess.call("mkdir -p /var/spool/postfix/var/run/courier/authdaemon", shell=True)
        subprocess.call("ln -s /var/run/courier/authdaemon/socket /var/spool/postfix/var/run/courier/authdaemon/socket", shell=True)
        subprocess.call("chown -R daemon:daemon /var/spool/postfix/var/run/courier", shell=True)
        subprocess.call("chmod 755 /var/spool/postfix/var/run/courier/authdaemon",shell=True)
    
    def deleteLinks(self):
        subprocess.call("rmdir /var/spool/postfix/var/run/mysqld", shell=True)
        subprocess.call("rmdir /var/spool/postfix/var/run/courier/authdaemon", shell=True)
        
    def createAll(self):
        self.createGroupAndUser()
        #~ self.changeMaster()
        self.createPostfixConfigFiles()
        #~ self.createLinks()
    
    def deleteAll(self):
        #~ self.deleteLinks()
        self.deletePostfixConfgFiles()
        self.deleteGroupAndUser()
        
        
        
        
        


