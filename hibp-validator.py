#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Automated validator for HIBP"""
"""Validates a list of email addresses against the HIBP website using the API""" 

__author__     = "Sam Bertram"
__version__     = "0.1"

hello_msg = '''
╦ ╦╦╔╗ ╔═╗  ╦  ╦┌─┐┬  ┬┌┬┐┌─┐┌┬┐┌─┐┬─┐
╠═╣║╠╩╗╠═╝  ╚╗╔╝├─┤│  │ ││├─┤ │ │ │├┬┘
╩ ╩╩╚═╝╩     ╚╝ ┴ ┴┴─┘┴─┴┘┴ ┴ ┴ └─┘┴└─
                                                 version: %s
                     
''' % __version__

data = {}


import re
import platform
import argparse
import datetime
import simplejson
import csv
import os
import urllib2
from random import randint
import pprint
import csv
import time

# GLOBALS
URL_BREACH = "https://haveibeenpwned.com/api/v2/breaches"
URL_SEARCH = "https://haveibeenpwned.com/api/v2/breachedaccount/"
#USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
USER_AGENT = "HIBP Validator"

# pretty print
pp = pprint.PrettyPrinter(indent=4)

# change opener User-Agent
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', USER_AGENT)]
urllib2.install_opener(opener)

parser = argparse.ArgumentParser(description="Work in progress...")
parser.add_argument('-t','--targets', help='File to read or target address. Includes @domain.com', required=True)
parser.add_argument('-o','--csv', help='File to write', default="output_hibp.csv")
parser.add_argument('-v','--verbose', help='Verbose output', action="store_true")
parser.add_argument('-vv','--debug', help='Less tool output, only shows good/bad/info error messages.', action="store_true")
parser.add_argument('-d','--delay',help="The delay between attempts (default 3000ms)", default=3000)
parser.add_argument('-j','--jitter',help="The delay jitter between attempts. Multiplied by sleep delay (default 0.2)", default=0.2)
parser.add_argument('-i','--index',help="Start from this count (index). Good for fast-forwarding through a file",default=False)

args = vars(parser.parse_args())

def main():

    print_time(time.time())

    # if debug is enabled, enable verbose as well 
    if args['debug']: args['verbose'] = True 
  
    # file options
    targets = args['targets']
    csv = args['csv']

    # timing options
    delay = int(args['delay'])
    jitter = float(args['jitter'])

    index = int(args['index'])

    if args['debug'] or args['verbose']:
      ALERT("targets: %s" % targets, ALERT.INFO)
      ALERT("time - delay: %s, jitter: %s" % (delay,jitter),ALERT.INFO)
      ALERT("csv: %s" % csv, ALERT.INFO)
      ALERT("URL_BREACH: %s" % URL_BREACH, ALERT.INFO)
      ALERT("URL_SEARCH: %s" % URL_SEARCH, ALERT.INFO)
      ALERT("USER_AGENT: %s" % USER_AGENT, ALERT.INFO)
      ALERT("index: %s" % index, ALERT.INFO)

    # try and validate the recipient, could be a single or could be a file
    if os.path.isfile(targets):
        ALERT("Recipient input is a file... reading")
        targets = open(targets).read().splitlines()
        ALERT("Testing multiple accounts (%s)" % len(targets))
    else:
        ALERT("Testing single account (%s)" % targets)
        targets = [targets]

    #emails = set(line.strip() for line in open(args['file']))

    count = 0
    for email in targets:
        count = count + 1
        
        if index and count < index: 
            continue

        hibp_result = "Not Validated"
        url = "%s%s" % (URL_SEARCH,email)
        if args['verbose']: ALERT("Requesting %s (%s/%s)..." % (url, count, len(targets)),ALERT.INFO)

        try:
            start = datetime.datetime.now()
            res = urllib2.urlopen(url)
            json = simplejson.loads(res.read())
                        
            if res.getcode() == 200:
                #if args['debug']: pp.pprint(json)
                pwned = ";".join(set(j['Title'] for j in json))
                hibp_result = pwned
            else:
                hibp_result = res
            
        except urllib2.HTTPError as e: hibp_result = str(e)

        if args['verbose']: ALERT("Result ... %s" % hibp_result)
        
        csvrow = "%s,%s,%s" % (start.strftime('%Y-%m-%d %H:%M:%S:%f'),email,hibp_result)
        if args['debug']:
            ALERT("CSV Result: %s" % csvrow, ALERT.INFO)

        fd = open(csv,'a')
        fd.write(csvrow)
        fd.write("\r\n")
        fd.close()

        snooze(delay,jitter)

    print_time(time.time())
    ALERT("done")

def snooze(delay,jitter):
    s = randint(int(delay)-(int(delay)*int(jitter)),int(delay)+(int(delay)*int(jitter)))
    if args['debug']: ALERT("Snoozing for %sms" % s, ALERT.INFO)
    time.sleep(s/1000)

def print_time(t):
    ALERT(datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'))

class ALERT(object):
    
    def __init__(self, message, level=0, spacing=0, ansi=True):

        # default to ansi alerting, if it's detected as windows platform then disable
        if platform.system() is "Windows": ansi = False

        good = '[+]'
        bad = '[-]'
        normal = '[*]'
        severe = '[!]'
        info = '[>]'
        space = ''

        for i in range(spacing):
            space += '  '
        
        if ansi == True:
            if level == ALERT.GOOD: print("%s%s%s%s" % ('\033[1;32m',good,"\033[0;0m",space)),
            elif level == ALERT.BAD: print("%s%s%s%s" % ('\033[1;31m',bad,"\033[0;0m",space)),
            elif level == ALERT.SEVERE: print("%s%s%s%s" % ('\033[1;31m',severe,"\033[0;0m",space)),
            elif level == ALERT.INFO: print("%s%s%s%s" % ('\033[1;33m',info,"\033[0;0m",space)),
            else: print("%s%s%s%s" % ('\033[1;34m',normal,"\033[0;0m",space)),
            
        else:
            if level == ALERT.GOOD: print('%s%s' % good,space),
            elif level == ALERT.BAD: print('%s%s' % bad,space),
            elif level == ALERT.SEVERE: print('%s%s' % (severe,space)),
            elif level == ALERT.INFO: print('%s%s' % (info,space)),
            else: print('%s%s' % normal,space),
            
        print message
    
    @staticmethod
    @property
    def BAD(self): return -1
        
    @staticmethod
    @property
    def NORMAL(self): return 0
        
    @staticmethod
    @property
    def GOOD(self): return 1

    @staticmethod
    @property
    def SEVERE(self): return -2

    @staticmethod
    @property
    def INFO(self): return 2

if __name__ == '__main__':
    print hello_msg
    main()



