#!/bin/python2.7
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import MySQLdb.cursors
import sys
import subprocess

sys.path[:0] = ['../']

import config

class useranddomain:
    
    def __init__(self):
        self.con = mdb.connect(host=config.mysqldomain, 
            port=config.mysqlport, user=config.mysqlpostfixuser, 
            passwd=config.mysqlpostfixpw, db=config.mysqlpostfixdb,
            cursorclass=MySQLdb.cursors.DictCursor)
            
    def addDomain(self,domain):
        cur = self.con.cursor()
        baserequest = "INSERT INTO domain (domain) VALUES (%s)"
        cur.execute(baserequest, (domain))
        subprocess.call("cd "+config.vmaildir+";mkdir "+domain,shell = True)
    
    def addAlias(self, go, to):
        cur = self.con.cursor()
        baserequest = "INSERT INTO alias (source,destination) VALUES (%s,%s)"
        cur.execute(baserequest, (go, to))
    
    def addUser(self, address, pw):
        cur = self.con.cursor()
        directory = address+"/"
        baserequest = "INSERT INTO mailbox (email, password)  VALUES (%s,ENCRYPT(%s))"
        cur.execute(baserequest, (address, pw))
        res = address.split("@") 
        subprocess.call("cd "+config.vmaildir+";cd "+res[1]+";maildirmake "+res[0], shell = True)
        subprocess.call("chown vmail:vmail -R "+config.vmaildir, shell = True)
    
    def __del__(self):
        self.con.close()
