import os
from setuptools import setup
from  browsermob import __version__ as version
setup(
    name = "bmob",
    version = version,
    author = "Rafael Ferreira",
    author_email = "raf@ophion.org",
    description = ("BrowserMob's API python client"),
    license =  'MIT/X11',
    keywords = "browsermob bmob api",
    url = "https://github.com/rferreira/bmob-python",
    packages=['browsermob'],
    long_description="BrowserMob's API python client",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Topic :: Utilities",
        'License :: OSI Approved :: MIT/X11'
    ],
    install_requires=['simplejson'],
    scripts=['scripts/bmob.py']
)
