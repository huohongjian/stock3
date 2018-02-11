#!/usr/bin/env python
# -*- coding:utf-8
# author: HuoHongJian
# date: 2018-01-05

import pandas as pd
import tushare as ts
from libs.Sqlite import Sqlite as db
from libs import tdate


pd.set_option('display.width', 1366)

def main(argString='600300'):
	code = argString

	sql = "SELECT code, price, change, volume, amount/10000 as amount, turnover, pe, \
		   name || ' ' || industry || ' ' || area as extrInfo\
   			FROM day_all WHERE code=?"
	df = db.conn().df(sql, [code])
	print(df)


	print('近期价格:')
	sql = "SELECT date, close, open, high, low, volume FROM kdata WHERE code=? ORDER BY date DESC LIMIT 5"
	df = db.conn().df(sql, [code])
	df.sort_values('date', inplace=True)
	print(df)
	exit()	

	sql = "SELECT max(date) FROM kdata"
	date = db.conn().val(sql)
	get_tick_data(code, date)





def get_tick_data(code, date):
	print('分笔数据:[date:{}]'.format(date))
	df = ts.get_tick_data(code, date=date)

	dfb = df[df['type']=='买盘'].sort_values(by='amount', ascending=False)
	dfs = df[df['type']=='卖盘'].sort_values(by='amount', ascending=False)
	_nb = dfb.shape[0]
	_ns = dfs.shape[0]
	_ab = dfb['amount'].sum()
	_as = dfs['amount'].sum()

	print('买盘: 成交笔数:{} [{:.2%}]  成交额:{} [{:.2%}]'.format(_nb, _nb/(_nb+_ns), _ab, _ab/(_ab+_as)))
	print(dfb.head(10))

	print('卖盘: 成交笔数:{} [{:.2%}]  成交额:{} [{:.2%}]'.format(_ns, _ns/(_nb+_ns), _as, _as/(_ab+_as)))
	dfs = dfs.head(10)
	dfs.loc['sum'] = dfs.apply(lambda x: x.sum())
	print(dfs.head(10))


if __name__ == '__main__':
	main()
