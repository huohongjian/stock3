#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, sys, time, argparse, getpass, datetime
from libs.Sqlite import Sqlite as db
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs import tdate

r = tdate.isTrade(tdate.yestday())

print(r, tdate.today())
print(tdate.nextTrade())
