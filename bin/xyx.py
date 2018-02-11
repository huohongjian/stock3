#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import pandas as pd
from libs.Sqlite import Sqlite as db
from libs import tdate, cache, parameter, dataFrame
from tqdm import tqdm


sqls = {'ds':'jbm', 'date':tdate.max(), 'days':'0', 'rate':'0.05,'}
filt = {}
disp = {}

def main(argString=''):
	global sqls, filt, disp
	sqls, filt, disp = parameter.parse(argString, sqls, filt, disp)

	codes = cache.codes.get(sqls.get('ds')) or []
	key = hash('xyx' + str(sqls) + str(codes))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		if sqls['days']=='0':
			df = once(sqls, filt, disp)
		else:
			df = many(sqls, filt, disp, codes)

		base = cache.get_stock_basics()
		df = pd.merge(df, base, on='code')
		cache.dfs.add(key, df)


	key = hash('xyx' + str(key) + str(filt))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		df = dataFrame.filter(df, filt)
		cache.dfs.add(key, df)
		cache.codes.save('xyx', df)


	dataFrame.render(df, **disp)
	parameter.render(sqls, filt, disp, df.shape[0])


	
def once(sqls, filt, disp):
	rate = parameter.extreme(sqls['rate'], ext=('0', '0.1'), toFloat=False)
	
	sql = "SELECT code, (close-low)/low AS rate FROM kdata WHERE date='{}' AND close<open AND (close-low)/low>={} AND (close-low)/low<={}"\
		.format(sqls['date'], rate[0], rate[1])
	df = db.conn().df(sql)
	return df



def many(sqls, filt, disp, codes):
	rate = parameter.extreme(sqls['rate'], ext=('0', '0.1'))

	df = pd.DataFrame(columns=['code', 'ndays'])
	conn = db.conn()
	pbar = tqdm(total=len(codes))
	for code in codes:
		pbar.set_description('[{}]'.format(code))
		pbar.update(1)

		sql = "SELECT close, low FROM kdata\
   				WHERE code='{}' AND date>='{}' AND date<='{}'"\
				.format()
		res = db.conn().all(sql)

		n = 0
		for r in res:
			_rate = (r['close']-r['low']) / r['low']
			if rate[0] <= _rate <= rate[1]:
				n += 1
		if n>0:
			df.append({
				'code': code,
				'ndays': n,			
			})

	return df



if __name__ == '__main__':
	main()
