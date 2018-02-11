#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time, getpass, readline
import pandas as pd
from ..Sqlite import Sqlite as db
from .. import cache



def main(customParas=''):
	c = cache.codes.save()
	cache.codes.list()
	cache.codes.render()
	print(c)
