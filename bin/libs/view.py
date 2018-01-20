#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import datetime
from .Sqlite import Sqlite as db


catch = {}

def basic(df):
	if catch.get('basic') is None:
		sql = '''SELECT a.code, a.pe, a.pb, a.esp, a.bvps,
			    b.price, (a.name||a.industry||a.area) as extrainfo
			    FROM stock_basics AS a
				LEFT JOIN day_all AS b
				ON a.code = b.code
				ORDER BY a.code'''
		
		catch['basic'] = db.conn().showsql().df(sql)
		print('catched')


	print(catch.get('basic').head())




def select(codes=[], order='code ASC', limit='0, 10'):
	titles = ['NO', 'code', 'pe', 'pb', 'esp', 'bvps', 'price', 'extra info']
	FM1 = '{:>3} {:>6} {:>7} {:>7} {:>7} {:>7} {:>7}  {}'
	FM2 = '{:>3} {:>6} {:>7.2f} {:>7.2f} {:>7.2f} {:>7.2f} {:>7.2f}  {} {} {}'

	sql = '''SELECT a.code, a.pe, a.pb, a.esp, a.bvps,
			b.price,
			a.name, a.industry, a.area
			FROM stock_basics AS a
			LEFT JOIN day_all AS b
			ON a.code=b.code
			WHERE a.code IN ({})
			ORDER BY a.{}
			LIMIT {}'''.format(str(codes)[1:-1], order, limit)
	res = db.conn().showsql().all(sql)

	print(FM1.format(*titles))
	i = 0
	for r in res:
		i += 1
		print(FM2.format(i, *r))




