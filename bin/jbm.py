#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import pandas as pd
from libs.Sqlite import Sqlite as db
from libs import cache, parameter, dataFrame

sqls = {}
filt = {}
disp = {}

def main(argString=''):
	global sqls, filt, disp
	sqls, filt, disp = parameter.parse(argString, sqls, filt, disp)

	key = hash('jbm' + str(filt))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		df = cache.get_stock_basics()
		df = dataFrame.filter(df, filt)
		cache.dfs.add(key, df)
		cache.codes.save('jbm', df)

	dataFrame.render(df, **disp)
	parameter.render(sqls, filt, disp, df.shape[0])


if __name__ == '__main__':
	main()
