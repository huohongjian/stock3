#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time 
import pandas as pd
from libs.Sqlite import Sqlite as db
from libs import tdate, cache, parameter, dataFrame



sql = "SELECT max(date) FROM kdata"
maxdate = db.conn().val(sql)

sqls = {'ma':'5,10', 'date':maxdate}
filt = {}
disp = {}

def main(argString=''):
	global sqls, filt, disp
	sqls, filt, disp = parameter.parse(argString, sqls, filt, disp)

	key = hash('ycx' + str(sqls))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		date = sqls.get('date')
		if not tdate.isTrade(date):
			print('The date you input is not trade day, please reset date parameter')
			return

		where = ''
		ns = sqls.get('ma').split(',')
		for n in ns:
			where += ' AND open<ma{0} AND close>ma{0}'.format(n)
		sql = "SELECT code, volume, ma5 FROM kdata WHERE date='" + date + "'" + where
		df = cache.exec(sql)
		base = cache.get_stock_basics()
		df = pd.merge(df, base, on='code')
		cache.dfs.add(key, df)


	key = hash('ycx' + str(key) + str(filt))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		df = dataFrame.filter(df, filt)
		cache.dfs.add(key, df)
		cache.codes.save('ycx', df)


	dataFrame.render(df, **disp)
	parameter.render(sqls, filt, disp, df.shape[0])



if __name__ == '__main__':
	main()
