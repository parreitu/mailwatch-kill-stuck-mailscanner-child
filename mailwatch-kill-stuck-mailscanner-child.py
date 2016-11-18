#!/usr/bin/python

import tailer
import re
import os
import signal
import time
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
# @reboot python /path-of-the-folder/scripts/mailwath-kill-stuck-mailscanner-child.py 

# I use my own log file to log each kill action that I have to commit
my_logfile = open('/tmp/mailwatch-kill-stuck-mailscanner-child.log','a')

# Follow the file as it grows
for line in tailer.follow(open('/var/log/mail.log')):
    if "Error: DBD::mysql::st execute failed" in line:
        response = re.search(r'^.*MailScanner\[(\d*)\].*', line)
        if response:
            pid = int(response.group(1))
            i = datetime.now()
            logfile.write(str("DateTime: " + str(i) + "-->  Killing problematic MailScanner child: " + str(pid) + '\n')) 
            os.kill(pid, signal.SIGTERM)

