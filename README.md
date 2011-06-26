# Bmob-Python

Python client to browsermob's API 

**For API documentation see http://cdn.browsermob.com/api.html**

	
## Install

To use bmob you will need python 2.5 or later
    
    python setup.py install
	
## Using the command line client

	$ bmob.py --indent -c fba125fcac31478a8748a9a09a216666:1234553 http://browsermob.com/a/m/all
	[
        {
            "accountId": 1234, 
            "alertEmail": null, 
            "browsers": [
                "FF3"
            ], 
            "deleted": false, 
            "email": "raf@ophion.org", 
            "enabled": true, 
            "frequency": 30, 
            "id": "b71f9d58c61c42f38de1e2f1835c00000", 
            "lastBilled": null, 
            "lastRun": 1305973284598, 
            "lastUpdated": 1309062529160, 
            "locations": [
                "NY"
            ], 
            "name": "ophion.org", 
            "preferenceId": "e8a08563910642218a287073e7dd53b5", 
            "scriptId": "40fd455d99264285afe5213b53f1a9f3"
        }, 

    ]

## API Example

To use bmob-python in your own python application, use the following logic:

    >>> from browsermob.api import BrowserMobAPI
    >>> client = BrowserMobAPI('fba125fcac31478a8748a9a09a2146325','12345')
    >>> client.call('http://browsermob.com/a/m/all',{})
    [{u'lastRun': 1305973284598, u'alertEmail': None, u'name': u'ophion.org', ...}]


## Authors

    raf@ophion.org
    pete@knewton.com