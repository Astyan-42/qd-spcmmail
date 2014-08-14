#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil

import config

class security:
    
    def __init__(self):
        pass
    
    def makeKey(self):
        subprocess.call("cd "+config.postfixdir+";openssl req -new -outform PEM -out smtpd.cert -newkey rsa:2048 -nodes -keyout smtpd.key -keyform PEM -days 3650 -x509",shell=True)
        subprocess.call("chmod o= "+os.path.join(config.postfixdir,"smtpd.key"),shell = True)
        
    def delKey(self):
        subprocess.call("cd "+config.postfixdir+";rm smtpd.*",shell = True)
        
    def createSmtpdConf(self):
        conf = open(os.path.join(config.postfixdir,"sasl","smtpd.conf"),"w")
        towrite = ["pwcheck_method: saslauthd\n",
        "mech_list: login plain\n"]
        #~ ["pwcheck_method: saslauthd\n",
        #~ "mech_list: login plain\n",
        #~ saslauthd_path: /var/spool/postfix/var/run/saslauthd/mux] in case of SASL authentication failure in /var/log/mail.log
        
        conf.writelines(towrite)
        
    def deleteSmtpdConf(self):
        try:
            os.remove(os.path.join(config.postfixdir,"sasl","smtpd.conf"))
        except:
            pass

    def replaceSASLAuth(self):
        conf = open(config.saslauthd[0],"w")
        conf.writelines(config.saslauthd[1])
        
    def createDiv(self):
        subprocess.call("mkdir -p /var/spool/postfix/var/run/saslauthd", shell = True)
        subprocess.call("chown -R root:sasl /var/spool/postfix/var/run/saslauthd", shell = True)
        subprocess.call("chmod 710 /var/spool/postfix/var/run/saslauthd", shell = True)
        subprocess.call("rm -rf /var/run/saslauthd",shell = True)
        subprocess.call("ln -s /var/spool/postfix/var/run/saslauthd /var/run/saslauthd", shell =  True)
        subprocess.call("adduser postfix sasl", shell = True)
        
    def deleteDiv(self):
        subprocess.call("rmdir /var/spool/postfix/var/run/saslauthd", shell = True)
        
    def createPamSmtp(self):
        conf = open(os.path.join("/","etc","pam.d","smtp"),"w")
        conf.writelines(config.pamsmtp)
        conf = open(os.path.join("/","etc","pam.d","smtpd"),"w")
        conf.writelines(config.pamsmtp)
    
    def deletePamSmtp(self):
        os.remove(os.path.join("/","etc","pam.d","smtp"))
        os.remove(os.path.join("/","etc","pam.d","smtpd"))
        
    def createAll(self):
        self.makeKey()
        self.createSmtpdConf()
        self.replaceSASLAuth()
        self.createDiv()
        self.createPamSmtp()
    
    def deleteAll(self):
        self.deletePamSmtp()
        self.deleteDiv()
        self.deleteSmtpdConf()
        self.delKey()
        
        
        
        
        
