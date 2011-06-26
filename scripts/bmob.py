#!/usr/bin/env python
# encoding: utf-8
import sys, os.path, logging, optparse 
import urllib2, urllib
import time, uuid
import base64, hmac, hashlib
import urlparse
import datetime

from browsermob.api import BrowserMobAPI
from browsermob import __version__ 

try:
	import json
except:
	import simplejson as json
	

log = logging.getLogger('bmob')

DESC = "BrowserMob's python command line client"	
		
if len(sys.argv) < 2:
	sys.argv.append('-h')

parser = optparse.OptionParser(usage="bmob.py [options] URL",description=DESC,version=__version__)

parser.add_option("-c","--cred", dest="cred", help="your API key and secret in KEY:SECRET format", action="store")
parser.add_option("-v","--verbose", dest="verbose", help="runs in verbose mode", action="store_true", default=False)
parser.add_option("-i","--indent", dest="indent", help="indents json output", action="store_true", default=False)
parser.add_option("-d","--data", dest="data", help="data to be sent with request in key=val mode", action="store", default=None)	


(options,args) = parser.parse_args()

# add ch to logger

if (options.verbose):
	ch = logging.StreamHandler()
	# create formatter
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	ch.setFormatter(formatter)
	log.setLevel(logging.DEBUG)		
	log.addHandler(ch)

if (options.cred is None):
	raise Exception('Please supply your credentials with -c KEY:SECRET')
	
key, secret =  options.cred.split(':')

# logging some info for debugging later
log.debug('python version: %s' % sys.version )

try: 
	import platform
	log.debug(platform.uname())
except:
	pass

# parsing data
params = {}
if options.data is not None:
	for p in options.data.split(','):
		k , v =  p.split('=')
		params[k] = v

	log.debug('params:')
	log.debug(params)
	
target = sys.argv[-1]

client = BrowserMobAPI(key,secret)

# performing the API call

start = time.time() * 1000
resp = client.call(target, params)
elapsed = time.time() * 1000  - start

log.debug('api response (%d ms elapsed): ' % elapsed)

if options.indent:
    print json.dumps(resp, sort_keys=True, indent=4)
    
else:
    print resp

		


