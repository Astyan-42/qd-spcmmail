#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import MySQLdb.cursors
import sys

import config

class mysqlpostfix:
    
    def __init__(self):
        self.con = mdb.connect(host=config.mysqldomain, 
            port=config.mysqlport, user=config.mysqlrootuser, 
            passwd=config.mysqlrootpw, 
            cursorclass=MySQLdb.cursors.DictCursor)
    
    def createPostfixDB(self):
        cur = self.con.cursor()
        baserequest = "CREATE DATABASE IF NOT EXISTS "+config.mysqlpostfixdb
        cur.execute(baserequest)
        self.con.select_db(config.mysqlpostfixdb)
    
    def createPostfixUser(self):
        cur = self.con.cursor()
        try:
            baserequest = "CREATE USER "+config.mysqlpostfixuser+" IDENTIFIED BY '"+config.mysqlpostfixpw+"'"
            cur.execute(baserequest)
        except:
            pass
        baserequest ="GRANT ALL PRIVILEGES ON "+config.mysqlpostfixdb+".* TO \""+config.mysqlpostfixuser+"\"@\"localhost\" IDENTIFIED BY '"+config.mysqlpostfixpw+"'"
        cur.execute(baserequest)
        
    def createTables(self):
        cur = self.con.cursor()
        try:
            for table in config.mysqltable:
                baserequest = table
                cur.execute(baserequest)
        except:
            sys.stderr.write("Something wrong append during the creation of mysql tables")
        
    def deleteAll(self):
        cur = self.con.cursor()
        baserequest = "DROP DATABASE IF EXISTS "+config.mysqlpostfixdb
        cur.execute(baserequest)
        baserequest = "DROP USER "+config.mysqlpostfixuser
        cur.execute(baserequest)
    
    def createAll(self):
        self.createPostfixDB()
        self.createPostfixUser()
        self.createTables()
    
    def __del__(self):
        self.con.close()
