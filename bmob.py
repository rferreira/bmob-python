#!/usr/bin/env python
# encoding: utf-8
import sys, os.path, logging, optparse 
import urllib2, urllib
import time, uuid
import base64, hmac, hashlib
import urlparse

try:
	import json
except:
	import simplejson as json
	

log = logging.getLogger('bmob')

__version__ = "0.2"
__license__ ="MIT/X11"

DESC = "BrowserMob's python command line client"

def sign(secret,url,params):
	"""Generates a BMOB friendly signature """
	
	data = 'POST' + '\n'
	data += urlparse.urlparse(url).hostname + '\n'
	data += urlparse.urlparse(url)[2] + '\n'
	

	urllib.urlencode(params)
	
	for k in sorted(params):
		data += '%s=%s&' %  ( k, params[k])
		
	# removing the trailing &
	data = data[:-1]
	
	log.debug('raw signature data:')
	log.debug(data)
	
	return base64.b64encode(hmac.new(secret, data, hashlib.sha1).digest())
	
def api_call(key,secret,url, params):
	"""http heavy lifting """
	
	data = {
		'key' : key,
		'timestamp': int(time.time() * 1000),
		'nonce' : str(uuid.uuid4()),			
	}
	
	if params is not None:
		data.update(params)
	
	# adding signature
	
	log.debug('combine data:')
	log.debug(data)
	
	data['signature'] = sign(secret,url,data)
		
	req = urllib2.Request(url, urllib.urlencode(data) )
	resp = urllib2.urlopen(req)	
	js = json.loads(resp.read())
	
	if js['oops'] is not None:
		raise Exception(js['oops'])
				
# main:
		
if len(sys.argv) < 2:
	sys.argv.append('-h')

parser = optparse.OptionParser(usage="bmob.py [options] URL",description=DESC,version=__version__)

parser.add_option("-c","--cred", dest="cred", help="your API key and secret in KEY:SECRET format", action="store")
parser.add_option("-v","--verbose", dest="verbose", help="runs in verbose mode", action="store_true", default=False)
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

# parsing data
params = {}
if options.data is not None:
	for p in options.data.split(','):
		k , v =  p.split('=')
		params[k] = v

	log.debug('params:')
	log.debug(params)
	
target = sys.argv[-1]

start = time.time() * 1000
resp = api_call(key,secret,target, params )
elapsed = time.time() * 1000  - start

log.debug('api response (%d msec elapsed): ' % elapsed)
print resp

		


