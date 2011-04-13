#!/usr/bin/env python
import sys
import os
import re
import subprocess

BASE_PATH = "/var/lib/denyhosts"
HOSTS_DENY = "/etc/hosts.deny"
DENYHOST_FILES = ['hosts', 'hosts-restricted', 'hosts-root', 'hosts-valid', 'users-hosts']
DENYHOSTS_STOP = "/etc/init.d/denyhosts stop"
DENYHOSTS_START = "/etc/init.d/denyhosts start"

args = sys.argv[1:]

if os.geteuid() != 0:
    print "You need to be a superuser to run this"
    sys.exit()

if len(args) <= 0:
    print "No IP addresses passed"
    print "Usage: sudo denyhosts-unban [ADDRESSES]"
    sys.exit()
    
stop_bits = DENYHOSTS_STOP.split()
subprocess.call(stop_bits)
    
for ip in args:
    print "Unbanning: %s..." % (ip)
    content = open(HOSTS_DENY, "r").read()
    regex = r"[a-zA-Z0-9]*\:\s%s\n" % (ip)
    rcontent = re.sub(regex, "", content)
    open(HOSTS_DENY, "w").write(rcontent)

    for afile in DENYHOST_FILES:
        path = os.path.join(BASE_PATH, afile)
        content = open(path, "r").read()
        regex = r"%s\:[0-9]\:.*\n" % (ip)
        rcontent = re.sub(regex, "", content)
        open(path, "w").write(rcontent)
        
start_bits = DENYHOSTS_START.split()
subprocess.call(start_bits)
print "Done"