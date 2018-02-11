#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: HuoHongJian
# date  : 2018-01-22

import re
import pandas as pd
from .Sqlite import Sqlite as db
from . import DataStruc


dfs = DataStruc.LinkedDict(maxLength=15)


def exec( sql, key=None):
	if key is None:
		key = hash(sql)
	if dfs.has(key):
		df = dfs.get(key)
	else:
		df = db.conn().df(sql)
		dfs.add(key, df)
	return df


def get_stock_basics(): 
	sql = '''SELECT a.code, b.price, b.p_change AS pcr, b.pe, a.pb, a.esp, a.bvps,
			(a.name||' '||a.industry||' '||a.area) as extrainfo
			FROM stock_basics AS a
			LEFT JOIN day_all AS b
			ON a.code = b.code
			ORDER BY a.code'''
	return exec(sql, 'base')


	
# cache the result of selected stock codes
class codes:
	_buffer = {}
	lastKey = None

	@classmethod
	def has(cls, key):
		return key in cls._buffer


	@classmethod
	def get(cls, key):
		return cls._buffer.get(key, {}).get('data')


	@classmethod
	def save(cls, key, df=None):
		if df is None:
			if dfs.getLast() is None:
				print('No codes cached. Please perform select stock command, and cache them.')
				return
			else:
				df = dfs.getLast()

		_codes = list(df.code)
		cls._buffer[key] = {
			'size':	len(_codes),
			'data': _codes,
		}
		cls.lastKey = key


	@classmethod
	def list(cls):
		print(' {:10} {:>5}\n{}'.format('cmd', 'size', '-'*20))
		for k, v in cls._buffer.items():
			print(' {:10} {:>5,}'.format(k, v.get('size')))


	@classmethod
	def detail(cls, key):
		pass



	@classmethod
	def union(cls):
		pass



