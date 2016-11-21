#!/usr/bin/python

import re
import os
import signal
import time
import sys
from datetime import datetime

# Author: Pedro Arreitunandia
# Code and last version https://github.com/parreitu/mailwatch-kill-stuck-mailscanner-child

# I don't know why, but some times per day I get this error in the mail.log file
# and as a consequence, MailScanner stops inserting new rows in the MySQL table so
# this information disappears from the Mailwatch page.
#
# MailScanner version = 5.0.3-7
# PHP Version = 5.6.28
# MySQL Version = 5.7.16
#
# This python script checks mail.log file and when it finds the error
# it gets the PID of the problematic MailScanner child and kills it
# 
# I call this scritp from the crontab after each reboot:
# @reboot python /path-of-the-folder/scripts/mailwatch-kill-stuck-mailscanner-child.py 

# I use my own log file to log each kill action that I have to commit

my_logfile = "/tmp/mailwath-kill-stucked-mailscanner-child.log"

f = open(my_logfile, 'a')
i = datetime.now()
f.write(str("============================================================= "  "\n"))
f.write(str("  DateTime: " + str(i) + "======================= "  "\n"))
f.write(str("============================================================= "  "\n"))
f.close()


mail_log_file  = subprocess.Popen(['tail','-F','/var/log/mail.log'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(mail_log_file.stdout)

while True:
    if p.poll(1):
        line = mail_log_file.stdout.readline()
        if "Error: DBD::mysql::st execute failed" in line:
            response = re.search(r'^.*MailScanner\[(\d*)\].*', line)
            if response:
                try:
                    f = open(my_logfile, 'a')
                    pid = int(response.group(1))
                    i = datetime.now()
                    f.write(str("DateTime: " + str(i) + "-->  Killing problematic MailScanner child: " + str(pid) + "\n")) 
                    f.close()
                    os.kill(pid, signal.SIGTERM)
                    f.close()
                except:
                     f.write(str("DateTime: " + str(i) + "-->  Exception: "+ sys.exc_info()[0] + "\n"))
                     f.close()
                     raise
