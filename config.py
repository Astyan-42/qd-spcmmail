#!/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys


mysqldomain = "localhost"
localdomain =  "127.0.0.1"
mysqlport = 3306

mysqlrootuser = "root"
mysqlrootpw = "rootpassword"

mysqlpostfixdb = "postfix"
mysqlpostfixuser = "postfix"
mysqlpostfixpw = "postfixpassword"

postfixdir = os.path.join("/","etc","postfix")
courierdir = os.path.join("/","etc","courier")

vmaildir = os.path.join("/","var","spool","vmail")
"""check that the gid and uid is free"""
vmailid = 5000

""" domain and acount to create during the installation """
domainstart = [ "domain1.tld", "domain2.tld" ]
usersstart = [ ("user@domain1.tld","password"), 
("user@domain2.tld","password") ]

"""You don't have to change what's following"""


mysqltablealias = """CREATE TABLE `alias` (
  `source` varchar(255) NOT NULL default '',
  `destination` text NOT NULL,
  `actif` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`source`)
) ENGINE=MyISAM COMMENT='Postfix Admin - Alias Virtuels';"""


mysqltabledomain = """CREATE TABLE `domain` (
  `domain` varchar(255) NOT NULL default '',
  `actif` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`domain`)
) ENGINE=MyISAM COMMENT='Postfix Admin - Domaines Virtuels';"""


mysqltablemailbox = """CREATE TABLE `mailbox` (
  `email` varchar(255) NOT NULL default '',
  `password` varchar(255) NOT NULL default '',
  `quota` int(10) NOT NULL default '0',
  `actif` tinyint(1) NOT NULL default '1',
  `imap` tinyint(1) NOT NULL default '1',
  `pop3` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`email`)
) ENGINE=MyISAM COMMENT='Postfix Admin - Boites Emails Virtuelles';"""
 

mysqltable = [ mysqltablealias, mysqltabledomain, mysqltablemailbox ]

postfixmaster = ["#\n",
"# Postfix master process configuration file.  For details on the format\n",
"# of the file, see the Postfix master(5) manual page.\n",
"#\n",
"# ==========================================================================\n",
"# service type  private unpriv  chroot  wakeup  maxproc command + args\n",
"#               (yes)   (yes)   (yes)   (never) (100)\n",
"# ==========================================================================\n",
"smtp      inet  n       -       n       -       -       smtpd\n",
"cleanup   unix  n       -       n       -       0       cleanup\n",
"rewrite   unix  -       -       n       -       -       trivial-rewrite\n"]


mysqlvirtual_domains = ("mysql-virtual_domains.cf",
["hosts = "+localdomain+"\n",
"user = "+mysqlpostfixuser+"\n",
"password = "+mysqlpostfixpw+"\n",
"dbname = "+mysqlpostfixdb+"\n",
"select_field = 'virtual'\n",
"table = domain\n",
"where_field = domain\n",
"additional_conditions = AND actif=1"])

mysqlvirtual_mailboxes = ("mysql-virtual_mailboxes.cf",
["hosts = "+localdomain+"\n",
"user = "+mysqlpostfixuser+"\n",
"password = "+mysqlpostfixpw+"\n",
"dbname = "+mysqlpostfixdb+"\n",
"select_field = CONCAT(SUBSTRING_INDEX(email,'@',-1),'/',SUBSTRING_INDEX(email,'@',1),'/')\n",
"table = mailbox\n",
"where_field = email\n",
"additional_conditions = AND actif=1\n"])

mysqlvirtual_aliases = ("mysql-virtual_aliases.cf",
["hosts = "+localdomain+"\n",
"user = "+mysqlpostfixuser+"\n",
"password = "+mysqlpostfixpw+"\n",
"dbname = "+mysqlpostfixdb+"\n",
"select_field = destination\n",
"table = alias\n",
"where_field = source\n",
"additional_conditions = AND actif=1"])

mysqlvirtual_aliases_mailbox = ("mysql-virtual_aliases_mailbox.cf",
["hosts = "+localdomain+"\n",
"user = "+mysqlpostfixuser+"\n",
"password = "+mysqlpostfixpw+"\n",
"dbname = "+mysqlpostfixdb+"\n",
"select_field = email\n",
"table = mailbox\n",
"where_field = email\n",
"additional_conditions = AND actif=1"])

mysqlvirtual_mailbox_limit_maps = ("mysql-virtual_mailbox_limit_maps.cf",
["hosts = "+localdomain+"\n",
"user = "+mysqlpostfixuser+"\n",
"password = "+mysqlpostfixpw+"\n",
"dbname = "+mysqlpostfixdb+"\n",
"select_field = quota\n",
"table = mailbox\n",
"where_field = email"])


postfixmain = ("main.cf",
["# /etc/postfix/main.cf\n",
"# Configuration Postfix\n",
"# espace.fr.to\n",
"#\n",
"\n",
"smtpd_banner = $myhostname ESMTP (Debian/GNU)\n",
"biff = no\n",
"disable_vrfy_command = yes\n",
"smtpd_helo_required = yes\n",
"\n",
"# ajoute le domaine aux emails de la distribution locale\n",
"# ainsi vous pourrez envoyer des emails sans @domain.priv\n",
"# par la commande sendmail\n",
"mydomain = domain.priv\n", 
"append_dot_mydomain = yes\n",
"\n",
"# Envoi une alerte de dépassement de délai par email\n",
"#delay_warning_time = 4h\n",
"\n",
"myhostname = smtp.domain.priv\n",
"\n",
"# domaine de distribution local\n",
"mydestination = localhost, localhost.localdomain\n",
"\n",
"# Mettez ici le relais smtp de votre FAI si vous avez des problèmes de blacklist\n",
"# à cause de votre IP\n",
"relayhost =\n",
"\n",
"# adresseIP/Masque des réseaux locaux (réseaux autorisés pour l'envoi de courier)\n",
"mynetworks = 127.0.0.0/8\n",
"inet_interfaces = all\n",
"\n",
"#restrictions d'accès\n",
"# adresses d'expédition\n",
"# le \"reject_unknown_sender_domain\" verifie que le domaine existe\n",
"smtpd_sender_restrictions =\n",
"        permit_mynetworks,\n",
"        reject_unknown_sender_domain,\n",
"        warn_if_reject reject_unverified_sender\n",
"\n",
"# adresses de destination\n",
"smtpd_recipient_restrictions =\n",
"        permit_mynetworks,\n",
"        permit_sasl_authenticated,\n", #
"        reject_non_fqdn_hostname,\n", #
"        reject_non_fqdn_sender,\n", #
"        reject_unauth_pipelining,\n", #  
"        reject_invalid_hostname,\n", #
"        reject_unauth_destination,\n",
"        reject_unknown_recipient_domain,\n",
"        reject_rbl_client list.dsbl.org,\n",#
"        reject_rbl_client bl.spamcop.net,\n",#
"        reject_rbl_client sbl-xbl.spamhaus.org\n",#
"        reject_non_fqdn_recipient\n",
"\n",
"# client\n",
"smtpd_client_restrictions =\n",
"        reject_unknown_client,\n",
"        permit_mynetworks\n",
"\n",
"virtual_alias_maps = mysql:"+os.path.join(postfixdir,mysqlvirtual_aliases[0])+",mysql:"+os.path.join(postfixdir,mysqlvirtual_aliases_mailbox[0])+"\n",
"virtual_mailbox_domains = mysql:"+os.path.join(postfixdir,mysqlvirtual_domains[0])+"\n",
"virtual_mailbox_maps = mysql:"+os.path.join(postfixdir,mysqlvirtual_mailboxes[0])+"\n",
"virtual_mailbox_base = "+vmaildir+"\n",
"virtual_uid_maps = static:"+str(vmailid)+"\n",
"virtual_gid_maps = static:"+str(vmailid)+"\n",
"\n",
"#virtual_create_maildirsize = yes\n",
"#virtual_mailbox_extended = yes\n",
"#virtual_mailbox_limit_maps = mysql:"+os.path.join(postfixdir,mysqlvirtual_mailbox_limit_maps[0])+"\n",
"#virtual_mailbox_limit_override = yes\n",
"#virtual_maildir_limit_message = \"Desole, la boite email de l'utilisateur est pleine, essayez plus tard.\"\n",
"#virtual_overquota_bounce = yes\n",
"\n",
"# Support TLS\n",
"smtpd_tls_cert_file = /etc/postfix/smtpd.cert\n",
"smtpd_tls_key_file = /etc/postfix/smtpd.key\n",
"\n",
" Support SASL\n",
"\n",
"broken_sasl_auth_clients = yes\n",
"smtpd_sasl_auth_enable = yes\n",
"smtpd_sasl_local_domain = $myhostname\n",
"smtpd_sasl_security_options = noanonymous\n",
"broken_sasl_auth_clients = yes\n",
"smtpd_sasl_type = cyrus\n",
"cyrus_sasl_config_path = /etc/postfix/sasl"])


postfixconfigfiles = [postfixmain, mysqlvirtual_domains,
mysqlvirtual_mailboxes, mysqlvirtual_aliases, 
mysqlvirtual_aliases_mailbox, mysqlvirtual_mailbox_limit_maps]


saslauthd = ( os.path.join("/","etc","default","saslauthd"),
["START=yes\n", "DESC=\"SASL Authentication Daemon\"\n",
"MECHANISMS=\"pam\"\n", "NAME=\"saslauthd\"\n", "MECH_OPTIONS=\"\"\n",
"THREADS=5\n",
"OPTIONS=\"-c -r -m /var/spool/postfix/var/run/saslauthd\""])

pamsmtp = [
"auth       required     pam_mysql.so user="+mysqlpostfixuser+" passwd="+mysqlpostfixpw+" host="+localdomain+" db="+mysqlpostfixdb+" table=mailbox usercolumn=email passwdcolumn=password crypt=1\n",
"account    sufficient   pam_mysql.so user="+mysqlpostfixuser+" passwd="+mysqlpostfixpw+" host="+localdomain+" db="+mysqlpostfixdb+" table=mailbox usercolumn=email passwdcolumn=password crypt=1"]

authmysqlrc = ["MYSQL_SERVER            "+localdomain+"\n",
"MYSQL_USERNAME          "+mysqlpostfixuser+"\n",
"MYSQL_PASSWORD          "+mysqlpostfixpw+"\n",
"#MYSQL_SOCKET           /var/lib/mysql/mysql.sock",
"MYSQL_PORT              "+str(mysqlport)+"\n",
"#MYSQL_OPT               0\n"
"MYSQL_DATABASE          "+mysqlpostfixdb+"\n",
"MYSQL_USER_TABLE        mailbox\n",
"MYSQL_CRYPT_PWFIELD     password\n",
"#DEFAULT_DOMAIN         domain.priv\n",
"MYSQL_UID_FIELD         "+str(vmailid)+"\n",
"MYSQL_GID_FIELD         "+str(vmailid)+"\n",
"MYSQL_LOGIN_FIELD       email\n",
"MYSQL_HOME_FIELD        \""+vmaildir+"\"\n",
"#MYSQL_NAME_FIELD        name\n",
"MYSQL_MAILDIR_FIELD     CONCAT(SUBSTRING_INDEX(email,'@',-1),'/',SUBSTRING_INDEX(email,'@',1),'/')\n",
"#MYSQL_QUOTA_FIELD      quota\n",
"#MYSQL_WHERE_CLAUSE     server='exemple.domain.tld'"]

authdaemonrc = [ "authmodulelist=\"authmysql\"\n",
"authmodulelistorig=\"authuserdb authpam authpgsql authldap authmysql authcustom authpipe\"\n",
"daemons=5\n",
"authdaemonvar=/var/run/courier/authdaemon\n",
"DEBUG_LOGIN=0\n",
"DEFAULTOPTIONS=\"\"\n",
"LOGGEROPTS=\"\""]

