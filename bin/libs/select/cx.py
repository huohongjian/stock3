#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time, getpass, readline
import pandas as pd
from ..Sqlite import Sqlite as db
from .. import cache
from .  import parameters


defaultParas = {
	'sort':	'code',
}

sqlParas = {
	'ma': '5,10'
}

def main(customParas):
	pd.set_option('display.width', 1366)
	
	for k in sqlParas:
		if customParas.get(k) is not None:
			sqlParas[k] = customParas.pop(k)
	
	where = ''
	ns = sqlParas.get('ma').split(',')
	for n in ns:
		where += ' AND open<ma{0} AND close>ma{0}'.format(n)
	sql = '''SELECT code, open, close, high, low, volume, ma5, ma10, ma20, ma30, ma60 FROM kdata
			WHERE date=(SELECT max(date) FROM kdata)''' + where

	df = cache.exec(sql)


	conditions, options = parameters.merge(defaultParas, customParas)
	df = cache.filter(df, conditions, 'ych')
	cache.render(df, **options)
	print(sqlParas)
	print(conditions)
	print(options, 'Total:[{:,}]'.format(df.shape[0]))


