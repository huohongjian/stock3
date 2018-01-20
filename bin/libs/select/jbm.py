#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time, getpass, readline
import pandas as pd
from ..Sqlite import Sqlite as db
from .. import view
from .. import cache
from .  import parameters


defaultParas = {
	'sort':	'pe',

	'pe':	',200',
	'esp':	'0.05,',
}

def main(customParas):
	conditions, options = parameters.merge(defaultParas, customParas)

	df = cache.get_stock_basics()
	df = cache.filter(df, conditions)
	cache.render(df, **options)
	print(conditions)
	print(options, 'Total:[{:,}]'.format(df.shape[0]))
	


def help():
	print('''
This is help content:

''')


