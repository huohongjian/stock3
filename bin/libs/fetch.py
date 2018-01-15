#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import datetime
from .Sqlite import Sqlite as db
from . import tdate
import tushare as ts


ENG = db.conn().connect

def get_k_data(code, start='2017-01-01', remove=True):
	if remove:
		sql = "DELETE FROM kdata WHERE code=?"
		db.conn().exec(sql, [code])

	try:
		df = ts.get_k_data(code, start=start)
		df = df.set_index('date')
	except Exception as e:
		print('[{}] some error raised:'.format(code), e)
	else:
		df['ma5'] = df.close.rolling(window=5).mean().round(2)
		df['ma10'] = df.close.rolling(window=10).mean().round(2)
		df['ma20'] = df.close.rolling(window=20).mean().round(2)
		df['ma30'] = df.close.rolling(window=30).mean().round(2)
		df['ma60'] = df.close.rolling(window=60).mean().round(2)
		
		df['va5'] = df.volume.rolling(window=5).mean().round()
		df['va10'] = df.volume.rolling(window=10).mean().round()
		df['va20'] = df.volume.rolling(window=20).mean().round()
		df['va30'] = df.volume.rolling(window=30).mean().round()
		df['va60'] = df.volume.rolling(window=60).mean().round()

		df.to_sql('kdata', ENG, if_exists='append')