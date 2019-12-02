#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2018, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://webscrapingbox.com"

import socket
hostname = socket.gethostname()
if 'MD104' in hostname:
    DEBUG=True
else:
    DEBUG=False


import threading
import requests as rq
import queue
from queue import Queue

import glob
import os
import zipfile
import sys
import time
import csv
import yaml
import os.path
import re
import random
import string
import logging
import requests as rq
from urllib.parse import urlparse
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import lxml.html
from xlrd import open_workbook
import configparser
import pickle
try:
    import Image
except ImportError:
    from PIL import Image


#  import time
#  ts = int(time.time())
#  print(ts)
# 1389177318

#=========================================== CONFIG GLOBAL =============================================================
#
## CONFIG LOG
#
globalLogLevel = logging.INFO
#globalLogLevel = logging.DEBUG
globalLogFormat = '%(asctime)s %(levelname)-4s %(filename)s:%(lineno)d %(message)s'
globalLogFile = 'app.log'
globalDateFmt = '%Y%m%d %H:%M:%S'

# Config loggin global
# set up logging to file - see previous section for more details
logging.basicConfig(level=globalLogLevel,
                    format=globalLogFormat,
                    datefmt=globalDateFmt,
                    filename=globalLogFile)

# Config log to console
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(globalLogLevel)
# set a format which is simpler for console use
formatter = logging.Formatter(globalLogFormat, datefmt=globalDateFmt)
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

#===========================================================================================================================
#COMMA
# CHECK IF FILE EXIST
# import os.path
# os.path.isfile(filePath) 


USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/20.6.14',
    'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; https://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.10) Gecko/20050716 Firefox/1.0.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; it-IT) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.3 Safari/534.34',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Version/3.1.2 Safari/525.21',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/534.51.22',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.27+ (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/125.5 (KHTML, like Gecko) Safari/125.9',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85.8.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.2 (KHTML, like Gecko) Safari/85.8',
]



''' How to use
    config = MyConfigParser("configFilePath").as_dict()
    username = config.get("config_info","username")
    write to config: config.set(section, key, value)
    '''
class MyConfigParser:
    def __init__(self, path):
        self._file_path = path
        self._config = configparser.ConfigParser()
        self._config.sections()
        self._config.read(path)
        
    def get(self, section, key):
        return self._config[section][key]

    def set(self, section, key, value):
        with open (self._file_path, 'w') as f:
            self._config[section, key, value]
            self._config.write(f)


def get_extension(file_name):
    ext = file_name.rsplit('.', 1)[1]
    return ext

def removeMoneySymbol(value):
    import pdb; pdb.set_trace()
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",",".")
    return value

def getQuantity(value):
    if value:
        value = re.findall(r'(\d+)', value, re.MULTILINE)
        if value:
            value = value[0]
        else:
            value = 0
    
    return value

def getMoney(value):
    if value is not None:
        trim = re.compile(r'[^\d.,]+')
        value = trim.sub('', value)
        value = value.replace(",","")
        return convertToFloat(value)
    else:
        return value
        
def convertToFloat(value):
    if value is None:
        return value
    try:
        return float(value)
    except ValueError:
        return None

def getFloatFromString(value):
    if value:
        value = re.findall(r'''([+-]?[0-9]*[.,]?[0-9]+)''', value, re.MULTILINE)
        if value:
            value = value[0]
            value.replace(',', '.')
            value = convertToFloat(value)
        else:
            value = None
    return value

def isValidUrl(url):
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not regex.match(url):
        return False
    else:
        return True
    

def extractEmails(url):
    response = rq.get(url)
    # print(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
    emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', response.text)
    if emails:
        for email in emails:
            if email not in emails:
                emails.append(email)
    return emails

def getDomainFromUrl(url, domainNameOnly = False):
    try:
        parsed_uri = urlparse(url.lower())
        if domainNameOnly:
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            domain = domain.replace('www.', '')
        else:
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain.replace(' ', '').replace('\n', '')
    except:
        logging.error("Fail to parse url %s: ", url)

def getCurrentDateString(format= '%Y-%m-%d %H:%M:%S'):
    ''' Get current date time string with format'''
    return time.strftime(format)

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print ('Please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False


def readTextFileToList(filePath):
    ''' Read text file line by line to list '''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    
    with open(filePath, encoding="utf8") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    return content

def readTextFile(filePath):
    ''' Read text file line by line to list '''
    content = ''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    
    with open(filePath, encoding="utf8") as f:
        content = f.read()
    
    return content

def readYamlFileToJson(filePath):
    ''' Read text file line by line to list '''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    jdata = None
    with open(filePath, encoding="utf8") as f:
        try:
            jdata = (yaml.safe_load(f))
        except yaml.YAMLError as exc:
            logging.info("Fail to parse Yaml file")
    return jdata
            

def writeListToTextFile(list, filePath, mode='a'):
    ''' Write list to csv line by line '''
    with open(filePath, mode, encoding="utf8") as myfile:
        for item in list:
            myfile.write(str(item) +  '\n')

def writeListToCsvFile(data, filename, mode='a', header = 'None'):
    ''' Write list to csv file '''
    with open(filename, mode,newline="", encoding="utf8") as f:
        writer = csv.writer(f, delimiter=',')
        if header:
            writer.writerow(header)
        writer.writerows(data)

def readXlsFileToDict(filePath):
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    if not os.path.isfile(filePath):
        filePath = os.path.join(CurrentPath, filePath)
    if not os.path.isfile(filePath):
        logging.info("readXlsFileToDict - File not found")
    book = open_workbook(filePath)
    sheet = book.sheet_by_index(0)
    # read header values into the list    
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
            for col_index in range(sheet.ncols)}
        dict_list.append(d)

    return dict_list

def readCsvToList(filePath):
    ''' Read csv file to list'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    with open(filePath, 'rb', encoding="utf8") as f:
        reader = csv.reader(f)
        return list(reader)

def readCsvToListDict(filePath):
    ''' Read csv file to list of dictionary'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []

    result = []
    with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
    
    with open(filePath, newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    
    return result, header

# def writeDictToCSV(dict_data, csvFilePath, mode='w'):
#     ''' Write list of dictionary to csv file'''
#     try:
#         isExistFile = os.path.isfile(csvFilePath)
#         keys = dict_data[0].keys()
#         with open(csvFilePath, mode,newline="", encoding="utf8") as f:
#             dict_writer = csv.DictWriter(f, keys)
#             if ('a' in mode) and isExistFile:
#                 pass
#             else:
#                 dict_writer.writeheader()

#             dict_writer.writerows(dict_data)
#         return True
#     except IOError as e:
#         logging.error("I/O error) %s", e)
#         return False
#     return True  


def writeDictToCSV(dict_data, csvFilePath, mode='w', headers=None):
    ''' Write list of dictionary to csv file'''
    try:
        isExistFile = os.path.isfile(csvFilePath)
        if not headers:
            headers = []
            for key in dict_data[0]:
                headers.append(key)

        with open(csvFilePath, mode,newline="", encoding="utf8") as f:
            writer = csv.writer(f)
            if ('a' in mode) and isExistFile:
                pass
            else:
                writer.writerow(headers)

            for row in dict_data:
                targetrow = []
                for key in headers:
                    targetrow.append(row[key])
                writer.writerow(targetrow)

        return True
    except IOError as e:
        logging.error("I/O error) %s", e)
        return False
    return True 

def getListFileWithExtension(file_path, ext = None):
    files = [f for f in glob.glob(file_path + "/" + str(ext), recursive=True)]
    return files

def getListFileInPath(dataPath, endwith = None):
    ''' Get list file in folder recusive '''
    result = []
    try:
        for root, dirs, files in os.walk(dataPath):
            for file in files:
                if endwith:
                    if file.endswith(endwith):
                        filename = os.path.join(root, file)
                        result.append(filename)
                else:
                    filename = os.path.join(root, file)
                    result.append(filename)
        return result
    except Exception as e:
        logging.error("Some thing wrong %s", e)
        return result
def removeHtmlTag(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def createFolderIfNotExists(folder_path):
    ''' Create a new folder if not exists'''
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def removeMoneySymbol(value):
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",","")
    return value

def getRandomString(n=20):
    ''' Return random string'''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))

def getRandomID(size=6, chars=string.ascii_uppercase + string.digits):
    ''' Return random string with number'''
    return ''.join(random.choice(chars) for _ in range(size))

def getUrlExtension(url):
    ''' Get extension of url'''
    ext = url.rsplit('.', 1)[1]
    return ext
def isAvailableUrl(url):
    '''
        Checking is url working or not
    '''
    result = False
    try:
        web = urlopen(url, timeout = 3.0)
        if web:
            code = web.getcode()
            result = code == 200
        else:
            result = False
    except:
        result = False
    return result


class WebBrowser():
    """Class web browser"""
    def __init__(self, currentPath=None, driver = None, 
        timeout = 10, isDisableImage = False, 
        isDisableJavascript = False, downloadPath = None, 
        isMaximum = False, isHeadless = False, 
        proxyArgsList = None, proxyIpList=None, changeProxyTotal=None, isMobile=False
        ):
        self._currentPath = currentPath
        self._driver = driver
        self._timeout = timeout
        self._isDisableImage = isDisableImage
        self._isDisableJavascript = isDisableJavascript
        self._downloadPath = downloadPath
        self._isHeadLess = isHeadless
        self._isMaximum = isMaximum
        self._proxyArgsList = proxyArgsList
        self._proxyIpList = proxyIpList
        self._changeProxyTotal = changeProxyTotal
        self._changeProxyCounter = 0
        self._isMobile = isMobile
        self._restartBrowserCounter = 0

        self.startBrowser()

    def getCookie(self):
        return self._driver.get_cookies()

    def saveCookie(self, filePath):
        pickle.dump( self._driver.get_cookies() , open(filePath,"wb"))
    
    def loadCookie(self, filePath):
        if os.path.isfile(filePath):
            cookies = pickle.load(open(filePath, "rb"))
            for cookie in cookies:
                self._driver.add_cookie(cookie)

    def getCurrentUrl(self):
        return self._driver.current_url

    def getPageSource(self):
        return self._driver.page_source
    
    # By Index
    # By Name or Id
    # By Web Element
    def switchToFrameByName(self, name, timeout=None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.NAME, name))
            )
            self._driver.switch_to_frame(name)
            return element
        except TimeoutException:
            logging.info(' Not found : %s', name)
            logging.debug('%s', TimeoutException)
            return None
        
    
    def switchToLastestWindow(self):
        # wait to make sure there are two windows open
        WebDriverWait(self._driver, 10).until(lambda d: len(d.window_handles) > 1)
        self._driver.switch_to_window(self._driver.window_handles[-1])
        # wait to make sure the new window is loaded
        WebDriverWait(self._driver, 10).until(lambda d: d.title != "")

    def closeCurrentWindows(self):
        self._driver.close()
        self._driver.switch_to_window(self._driver.window_handles[-1])

    
    def findVisibleByXpath(self, locator, timeout=None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None
        

    def findByXpath(self, locator, timeout = None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None

    def findByXpathFromElement(self, sel, locator , timeout = None):
        ''' Get one item by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(sel, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return None

    def findAllByXpath(self, locator, timeout = None):
        ''' Get all items by xpath'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            logging.info(' Find by xpath not found : %s', locator)
            logging.debug('%s', TimeoutException)
            return []

    def findByClass(self, classname, timeout = None):
        ''' Get one item by class'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, classname)))
            return element
        except TimeoutException:
            logging.info(' Find by class not found : %s', classname)
            logging.debug('%s', TimeoutException)
            return None
            
    def findAllByClass(self, classname, timeout = None):
        ''' Get all item by class'''
        if not timeout:
            timeout = self._timeout
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, classname)))
            return element
        except TimeoutException:
            logging.info(' Find by class not found : %s', classname)
            logging.debug('%s', TimeoutException)
            return []
    
    def selectDropdownByText(self, locator, text_value, timeout = None):
        tag = self.findByXpath(locator)
        if tag:
            select = Select(tag)
            select.select_by_visible_text(text_value)
        else:
            logging.info('Not found dropdown at xpath {}'.format(locator))
    
    def selectDropdownByValue(self, locator, value, timeout = None):
        tag = self.findByXpath(locator)
        if tag:
            select = Select(tag)
            select.select_by_value(value)
        else:
            logging.info('Not found dropdown at xpath {}'.format(locator))
    
    def selectDropdownByValue(self, locator, index, timeout = None):
        tag = self.findByXpath(locator)
        if tag:
            select = Select(tag)
            select.select_by_index(index)
        else:
            logging.info('Not found dropdown at xpath {}'.format(locator))
            
    def isExistByXPath(self, locator, timeout = None):
        ''' Check if xpath is exists'''
        if not timeout:
            timeout = self._timeout
        try:
            WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False
        return True

                    
    def restartDriver(self):
        ''' Restart the browser'''
        logging.info("Restart browser")
        if self._driver:
            self._driver.close()
        time.sleep(1)
        self.startBrowser()

    def exitDriver(self):
        ''' Exit the browser'''
        logging.info("Exit browser")
        if self._driver:
            self._driver.close()

    def getUrl(self, url):
        if self._changeProxyTotal:
            self._changeProxyCounter+=1
            if self._changeProxyCounter > self._changeProxyTotal:
                self.restartDriver()
                self._changeProxyCounter = 0
        ''' Get an url '''
        try:
            self._driver.get(url)
            if self.hasCaptcha():
                logging.info("Page has captcha. Restart browser")
                self.restartDriver()
                self._restartBrowserCounter += 1
                if self._restartBrowserCounter > 5:
                    self._restartBrowserCounter = 0
                    # Skip this url
                    return False
                self.getUrl(url)
            return True
        except:
            logging.info("Fail to get %s", url)
            print("Unexpected error:", sys.exc_info()[0])
            return False
        
        
    
    def hasCaptcha(self):
        time.sleep(1)
        pagesource = self.getPageSource()


        if 'Blocked IP Address' in pagesource or 'recaptcha-token' in pagesource or 'I am not a robot' in pagesource\
        or 'not a robot' in pagesource or 'Enter the characters you see below' in pagesource or 'Sorry! Something went wrong on our end' in pagesource:
            logging.info("Has captcha")
            return True
        else:
            return False
    
    def executeJavaScript(self,jsString):
        logging.info("Execute script {}".format(jsString))
        self._driver.execute_script(jsString)
        time.sleep(1)
    
    def scrollDown(self, number = 10):
        for i in range(0, number):
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    def scrollUp(self, number = 10):
        for i in range(0, number):
            self._driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
            time.sleep(1)
    def scrollTop(self):
        self._driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    
    def scrollInfinity(self, iretry = 15):
        # scroll infinity
        # define initial page height for 'while' loop
        last_height = self._driver.execute_script("return document.body.scrollHeight")
        logging.info("Scrolling down ... ")
        retry = iretry
        page = 0
        while True:
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = self._driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                retry -= 1
                if retry < 0:
                    break
            else:
                last_height = new_height
                page += 1
                logging.info("Scroll down page: %d", page)
                retry = iretry

    def clickOnFly(self, element, moveTimeout=1):
        ''' Click coordiate'''
        hover = ActionChains(self._driver).move_to_element(element).move_by_offset(10, 10).click()
        hover.perform()
    
    def dismiss_alert(self):
        try:
            WebDriverWait(self._driver, 2).until(EC.alert_is_present())
            self._driver.switch_to_alert().accept()
            return True
        except TimeoutException:
            return False
        
    def getScreenShotByXpath(self, xpath, result_path):
        element = self.findByXpath(xpath)
        if not element:
            logging.info("Not found element at xpath: %d", xpath)

        location = element.location
        size = element.size

        self._driver.save_screenshot("temp.png")

        x = location['x']
        y = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']

        im = Image.open('temp.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save(result_path)
        # Delete temp image
        if os.path.isfile('temp.png'):
            os.remove('temp.png')
            
        return result_path

    def hoverElement(self, element, moveTimeout=1):
        ''' Hover an element'''
        hover = ActionChains(self._driver).move_to_element(element)
        hover.perform()

    def clickElement(self, element, moveTimeout=1):
        try:
            ''' Click an element'''
            actions = ActionChains(self._driver)
            actions.move_to_element(element)
            actions.perform()
            time.sleep(moveTimeout)
            actions.click(element)
            actions.perform()
            return True
        except:
            logging.info("Can't click element")
            return False

    def sendKeys(self, key):
        ''' Send key to brower'''
        actions = ActionChains(self._driver)
        actions.send_keys(key)
        actions.perform()

    def getPlugin(self, proxy_host, proxy_port, proxy_user, proxy_pass):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        return pluginfile

    def startBrowser(self):
        ''' Start the browser'''
        logging.info("Start browser")

        chromeOptions = webdriver.ChromeOptions()

        if self._proxyArgsList:
            chromeOptions.add_extension(self.getPlugin(**random.choice(self._proxyArgsList)))
        
        if self._proxyIpList:
            proxyip = random.choice(self._proxyIpList)
            logging.info("proxy ip: {}".format(proxyip))
            chromeOptions.add_argument('--proxy-server={}'.format(proxyip))

        if self._isHeadLess:
            logging.info('Start browser in headless mode')
            chromeOptions.add_argument("--headless")
            chromeOptions.add_argument("--disable-gpu") 

        if DEBUG:
            chromeOptions.add_extension("chropath.zip")
        
        # chromeOptions.add_argument('--disable-extensions')
        # chromeOptions.add_argument('--profile-directory=Default')
        # chromeOptions.add_argument("--incognito")
        # chromeOptions.add_argument("--disable-plugins-discovery");
        # chromeOptions.add_argument("--start-maximized")
        # chromeOptions.add_argument("--no-experiments")
        chromeOptions.add_argument("--disable-translate")
        # chromeOptions.add_argument("--disable-plugins")
        # chromeOptions.add_argument("--disable-extensions");
        # chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--disable-setuid-sandbox")
        chromeOptions.add_argument("--no-default-browser-check")
        # chromeOptions.add_argument("--clear-token-service")
        chromeOptions.add_argument("--disable-default-apps")
        
        chromeOptions.add_argument('user-agent={}'.format(random.choice(USER_AGENT_LIST)))
        chromeOptions.add_argument("test-type")
        chromeOptions.add_argument('--log-level=3')
        
        if(self._isMaximum):
            chromeOptions.add_argument("start-maximized")
        
        prefs = { "profile.default_content_setting_values.notifications": 2 }
        
        if self._isDisableImage:
            prefs["profile.managed_default_content_settings.images"] = 2

        if self._isDisableJavascript:
            prefs["profile.managed_default_content_settings.javascript"] = 2
        
        chromeOptions.add_experimental_option("prefs",prefs)
        # chromeOptions.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

        if self._downloadPath:
            prefs = {'plugins': {'plugins_disabled': ['Chrome PDF Viewer']}, 'download': {'default_directory': self._downloadPath, "directory_upgrade": True}}

        if os.name == 'posix':
            if self._currentPath:
                chromedriver=os.path.join(self._currentPath,"chromedriver")
            else:
                chromedriver='chromedriver'
        else:
            if self._currentPath:
                chromedriver=os.path.join(self._currentPath,"chromedriver.exe")
            else:
                chromedriver='chromedriver.exe'
        
        if self._isMobile:
            mobile_emulation = {
                "deviceMetrics": { "width": 414, "height": 716, "pixelRatio": 3.0 },
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
            
            chromeOptions.add_experimental_option("mobileEmulation", mobile_emulation)


        # desired_cap = {
        #     'browserName': 'safari',
        #     'version': '12.0',
        #     'platform': 'iOS',
        #     'deviceName': 'iPhone X',
        #     'platformName': 'iOS',
        #     'name' : 'My First Mobile Test',
        #         }

        # self._driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions,desired_capabilities=desired_cap)
        self._driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

        # self._driver.delete_all_cookies()
        
        if self._isMobile:
            self._driver.set_window_size(414,716)
        # self._driver.set_window_position(0,0)
        #driver.set_window_position(-10000,0)
        self._driver.switch_to_window(self._driver.current_window_handle)


    def tryClick(self, element, num = 10):
        ''' Try to click an element'''
        is_clicked = False
        step = 0
        while not is_clicked and step < num:
            try:
                is_clicked = self.clickElement(element, 5)
                is_clicked = True
            except: 
                time.sleep(1)
                logging.info("try click %s", element)
                is_clicked = False
            step+=1
        
        return is_clicked

    
    def tryClickByXpath(self, locator, num = 10):
        ''' Try to click an element'''
        is_clicked = False
        retry = num
        while not is_clicked and num > 0:
            num -= 1
            element = self.findByXpath(locator)
            if element:
                is_clicked = self.clickElement(element, moveTimeout=retry-num)
                if is_clicked:
                    return True
            # Else try click again    
            time.sleep(1)
            logging.info("try click {} x {}".format(num, locator))
        
        return is_clicked


class ThreadedDownload(object):
    '''
        Download images with multi thread
        How to use

        downloader = ThreadedDownload(urls, ".", True, 10, 2)
        # urls = list[imageUrl, downloadFilePath]
        print 'Downloading %s files' % len(urls)
        downloader.run()
        # print report
        print 'Downloaded %(success)s of %(total)s' % {'success': len(downloader.report['success']), 'total': len(urls)}
        
        if len(downloader.report['failure']) > 0:
            print '\nFailed urls:'
            for url in downloader.report['failure']:
                print url
    '''
    REGEX = {
        'hostname_strip':re.compile('.*\..*?/', re.I)
    }
    
    
    class MissingDirectoryException(Exception):
        pass
    
        
    class Downloader(threading.Thread):
        def __init__(self, queue, report):
            threading.Thread.__init__(self)
            self.queue = queue
            self.report = report
        
        def run(self):
            while self.queue.empty() == False:
                url = self.queue.get()
                
                response = url.download()
                if response == False and url.url_tried < url.url_tries:
                    self.queue.put(url)
                elif response == False and url.url_tried == url.url_tries:
                    self.report['failure'].append(url)
                elif response == True:
                    self.report['success'].append(url)
                
                self.queue.task_done()
    
    
    class URLTarget(object):
        def __init__(self, url, destination, url_tries):
            self.url = url
            self.destination = destination
            self.url_tries = url_tries
            self.url_tried = 0
            self.success = False
            self.error = None
        
        def download(self):
            self.url_tried = self.url_tried + 1
            
            try:
                if os.path.exists(self.destination): # This file has already been downloaded
                    self.success = True
                    return self.success
                
                remote_file = urlopen(self.url)
                package = remote_file.read()
                remote_file.close()
                
                if os.path.exists(os.path.dirname(self.destination)) == False:
                    os.makedirs(os.path.dirname(self.destination))
                
                dest_file = open(self.destination, 'wb')
                dest_file.write(package)
                dest_file.close()
                
                self.success = True
                
            except Exception as e:
                self.error = e
                
            return self.success
        
        def __str__(self):
            return 'URLTarget (%(url)s, %(success)s, %(error)s)' % {'url':self.url, 'success':self.success, 'error':self.error}
    
    
    def __init__(self, urls=[], destination='.', directory_structure=False, thread_count=5, url_tries=3):
        if os.path.exists(destination) == False:
            raise ThreadedDownload.MissingDirectoryException('Destination folder does not exist.')
        
        self.queue = Queue(maxsize=0) # Infinite sized queue
        self.report = {'success':[],'failure':[]}
        self.threads = []
        
        if destination[-1] != os.path.sep:
            destination = destination + os.path.sep
        self.destination = destination
        self.thread_count = thread_count
        self.directory_structure = directory_structure
        
        # Prepopulate queue with any values we were given
        for url in urls:
            self.queue.put(ThreadedDownload.URLTarget(url[0], url[1], url_tries))
    
    
    def fileDestination(self, url):
        if self.directory_structure == False:
            # No directory structure, just filenames
            file_destination = '%s%s' % (self.destination, os.path.basename(url))
        
        elif self.directory_structure == True:
            # Strip off hostname, keep all other directories
            file_destination =  '%s%s' % (self.destination, ThreadedDownload.REGEX['hostname_strip'].sub('', url))
        
        elif hasattr(self.directory_structure, '__len__') and len(self.directory_structure) == 2:
            # User supplied a custom regex replace
            regex = self.directory_structure[0]
            if isinstance(regex, str):
                regex = re.compile(str)
            replace = self.directory_structure[1]
            file_destination =  '%s%s' % (self.destination, regex.sub(replace, url))
        
        else:
            # No idea what's wanted
            file_destination = None
        
        if hasattr(file_destination, 'replace'):
            file_destination = file_destination.replace('/', os.path.sep)
        return file_destination
    
    
    def addTarget(self, url, url_tries=3):
        self.queue.put(ThreadedDownload.URLTarget(url, self.fileDestination(url), url_tries))
    
    
    def run(self):
        for i in range(self.thread_count):
            thread = ThreadedDownload.Downloader(self.queue, self.report)
            thread.start()
            self.threads.append(thread)
        if self.queue.qsize() > 0:
            self.queue.join()