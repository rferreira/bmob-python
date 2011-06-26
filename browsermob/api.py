#!/usr/bin/env python
# encoding: utf-8
import logging
import urllib2, urllib
import time, uuid
import base64, hmac, hashlib
import urlparse
import datetime

try:
	import json
except:
	import simplejson as json
	
log = logging.getLogger('bmob')

class BrowserMobAPI:
	def __init__(self, key, secret):
		self.secret = secret
		self.key = key
	
	def _sign(self, secret, url, params):
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
	
	def _default_times(self, params):
		"""sets default times in the params dictionary if none are set. """
		if ("end" not in params):
			params["end"] = int(time.time() * 1000)
			if ("resolution" not in params):
				params["resolution"] = "hour"
		
		if ("start" not in params):
			params["start"] = int(params["end"] - (24 * 3600 * 1000))

	def call(self, url, params):
		"""http heavy lifting """
		
		data = {
			'key' : self.key,
			'timestamp': int(time.time()*1000),
			'nonce' : str(uuid.uuid4()),
		}
		
		if params is not None:
			self._default_times(params)
			data.update(params)
		
		# adding signature
		
		log.debug('combine data:')
		log.debug(data)
		
		data['signature'] = self._sign(self.secret, url, data)
			
		req = urllib2.Request(url, urllib.urlencode(data) )
		resp = urllib2.urlopen(req)
		js = json.loads(resp.read())
		
		log.debug('raw response:')
		log.debug(js)
		
		if 'oops' in js:
			raise Exception(js['oops'])
		
		return js

