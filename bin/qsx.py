#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import os, time, datetime
import pandas as pd
from tqdm import tqdm
from libs.Sqlite import Sqlite as db
from libs import cache, parameter, dataFrame


sqls = {'ds':None, 'nday':'500', 'nlow':'0,150', 'grow':',0.3', 'lhr':',0.6'}
filt = {}
disp = {}

def main(argString=''):
	global sqls, filt, disp
	sqls, filt, disp = parameter.parse(argString, sqls, filt, disp)

	if sqls.get('ds') is None:
		sqls['ds'] = cache.codes.lastKey

	codes = cache.codes.get(sqls.get('ds')) or []
	key = hash('qsx' + str(sqls) + str(codes))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		
		nday = sqls.get('nday')
		nlow1, nlow2 = parameter.extreme(sqls.get('nlow'), ('0',nday), isMax=True, toFloat=True)
		grow1, grow2 = parameter.extreme(sqls.get('grow'), ('0', '1'), isMax=True, toFloat=True)
		lhr1,  lhr2  = parameter.extreme(sqls.get('lhr'),  ('0', '1'), isMax=True, toFloat=True)
	
		today = datetime.datetime.now()
		day1 = today - datetime.timedelta(days=nlow2)
		day2 = today - datetime.timedelta(days=nlow1)

		df = pd.DataFrame(columns=['code', 'mHigh', 'mLow', 'lhr', 'grow'])
		conn = db.conn()
		pbar = tqdm(total=len(codes))
		for code in codes:
			pbar.set_description('[{}]'.format(code))
			pbar.update(1)

			sql = "SELECT min(low), max(high) FROM kdata WHERE code=? ORDER BY date DESC LIMIT ?"
			minLow, maxHigh = db.conn().one(sql, [code, nday])
			lhr = minLow / maxHigh
			if lhr<lhr1 or lhr>lhr2:
				continue

			sql = "SELECT close FROM kdata WHERE code=? ORDER BY date DESC LIMIT 1"
			price = db.conn().val(sql, [code])
			grow = (price - minLow) / minLow
			if grow<grow1 or grow>grow2:
				continue

			sql = "SELECT date FROM kdata WHERE code=? AND low=?"
			minDate = db.conn().val(sql, [code, minLow])
			day = datetime.datetime.strptime(minDate, '%Y-%m-%d')
			if day<day1 or day>day2:
				continue

			df = df.append({
					'code':code,
				   	'mHigh': round(maxHigh, 2),
				   	'mLow':  round(minLow,  2),
			   		'grow':  round(grow*100,1),
				   	'lhr':   round(lhr*100, 1)
				}, ignore_index=True)
		pbar.close()
		base = cache.get_stock_basics()
		df = pd.merge(df, base, on='code')
		cache.dfs.add(key, df)

	key = hash('qsx' + str(key) + str(filt))
	if cache.dfs.has(key):
		df = cache.dfs.get(key)
	else:
		df = dataFrame.filter(df, filt)
		cache.dfs.add(key, df)
		cache.codes.save('qsx', df)

	dataFrame.render(df, **disp)
	parameter.render(sqls, filt, disp, df.shape[0])
	return
#		sql = '''SELECT code, date, open, close, high, low
#				FROM kdata WHERE code=? ORDER BY date LIMIT ?'''
#		df = conn.df(sql, [code, int(during)])

#		if df.shape[0] == 0:
#			continue
#		curRow = df.iloc[-1]
#		lowRow = df[df.low == df.low.min()].iloc[0]
#		higRow = df[df.hight == df.hight.max()]
		
#		price = curRow.close
#		lowPrice = lowRow.low

#		lowDate = datetime.datetime.strptime(lowRow.date, '%Y-%m-%d')
#		if lowDate>day1 and lowDate<day2 and price>lowPrice*(1+growth1) and price<lowPrice*(1+growth2):
#			res.append(code)

	

if __name__ == '__main__':
	main()
