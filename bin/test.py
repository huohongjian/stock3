#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

#import os, sys, time, argparse, getpass, datetime
#from libs.Sqlite import Sqlite as db
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from libs import tdate
#from libs import fetch
#import pandas as pd
#import numpy as np
#from tqdm import tqdm
#from libs import common as co
#from libs import view

from libs import cache

for i in range(15):
	cache.add('a'+str(i), 'data'+str(i))

d = cache.get('a9')
